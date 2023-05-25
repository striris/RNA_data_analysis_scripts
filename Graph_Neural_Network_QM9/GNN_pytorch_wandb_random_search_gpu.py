#!/usr/bin/env python
# coding: utf-8
from torch_geometric.datasets import QM9
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import logging
import time
import wandb
wandb.login()
import random

import os.path as osp

import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.nn import GRU, Linear, ReLU, Sequential
import torch.optim as optim

import torch_geometric.transforms as T
from torch_geometric.datasets import QM9
from torch_geometric.loader import DataLoader
from torch_geometric.nn import NNConv, Set2Set, MessagePassing, global_mean_pool, aggr,GCNConv
from torch_geometric.utils import remove_self_loops

model_name = "adam_mse_gcnconv_poolMaxAggr_2fc_wandb_random_gpu"

import wandb
import numpy as np 
import random
device = torch.device('cuda:4' if torch.cuda.is_available() else 'cpu')
print(torch.cuda.is_available())
print(device)
# Define sweep config
sweep_configuration = {
'method': 'random',
'metric': {'goal': 'minimize', 'name': 'val_loss'},
'parameters': {'batch_size': {'distribution': 'q_log_uniform_values',
                               'max': 256,
                               'min': 16,
                               'q': 8},
                'criterion': {'value': 'MSELoss()'},
                'epochs': {'values': [20,40,60,80]},
                'hidden_dim_1': {'value': 64},
                'hidden_dim_2': {'value': 128},
                'hidden_dim_3': {'value': 32},
                'in_channels': {'value': 11},
                'lr': {'distribution': 'uniform',
                                  'max': 0.1,
                                  'min': 0},
                'optimizer': {'value': 'adam'},
                'out_channels': {'value': 1}
              }
}

# Initialize sweep by passing in config. 
# (Optional) Provide a name of the project.
sweep_id = wandb.sweep(
  sweep=sweep_configuration, 
  project=model_name
  )

# Define the dataset and do transformation
class TargetTransform:
    def __call__(self, data):
        # Specify target.
        target = 0 # the first property is the one to be predicted
        data.y = data.y[:, target]
        return data
    
def data(bs):
    path = './datasets/QM9'
    transform = T.Compose([TargetTransform(), T.Distance(norm=False)]) # add the distance into edge attributes
    dataset = QM9(path, transform=transform)
    # Split datasets.
    torch.manual_seed(12345)
    dataset = dataset.shuffle()
    test_dataset = dataset[:10000]
    val_dataset = dataset[10000:20000]
    train_dataset = dataset[20000:]
    test_loader = DataLoader(test_dataset, batch_size=bs, shuffle=False) #10000
    val_loader = DataLoader(val_dataset, batch_size=bs, shuffle=False) #10000
    train_loader = DataLoader(train_dataset, batch_size=bs, shuffle=True) #110831
    return test_loader, train_loader, val_loader

# Define training function that takes in hyperparameter 
# values from `wandb.config` and uses them to train a 
# model and return metric
def train_one_epoch(device, model, train_loader, epoch, lr, optimizer): 
    # Train step
    model.train()
    total_loss = 0
    for batch in train_loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        output = model(batch).flatten()
        loss = nn.MSELoss()
        loss_output = loss(output, batch.y)
        loss_output.backward()
        optimizer.step()
        total_loss += loss_output * batch.num_graphs

    average_loss = total_loss  / len(train_loader.dataset)
    
    print(f'Epoch: {epoch}, Training Loss: {average_loss:.4f}')
    logging.info(f'Epoch: {epoch}, Training Loss: {average_loss:.4f}')
    
    return average_loss

def evaluate_one_epoch(device, model, val_loader, epoch, lr): 
    # Validation step
    model.eval()
    total_val_loss = 0

    with torch.no_grad():
        for data in val_loader:
            data = data.to(device)
            output = model(data).flatten()
            val_loss = nn.MSELoss()
            val_loss_output = val_loss(output, data.y)
            total_val_loss += val_loss_output * data.num_graphs

    average_val_loss = total_val_loss / len(val_loader.dataset)
    
    print(f'Epoch: {epoch}, Validation Loss: {average_val_loss:.4f}')
    logging.info(f'Epoch: {epoch}, Validation Loss: {average_val_loss:.4f}')
    
    return average_val_loss

# Define the GNN model
class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_dim_1, hidden_dim_2, hidden_dim_3, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_dim_1)
        self.conv2 = GCNConv(hidden_dim_1, hidden_dim_2)
        self.global_pool = aggr.MaxAggregation()
        self.fc1 = nn.Linear(hidden_dim_2, hidden_dim_3)
        self.fc2 = nn.Linear(hidden_dim_3, out_channels)

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.global_pool(x,batch)
        x = self.fc1(x).relu()
        x = self.fc2(x)

        return x
    
def build_model(in_channels, hidden_dim_1, hidden_dim_2, hidden_dim_3, out_channels):
    # Initialize the model, optimizer, and loss function
    model = GCN(in_channels, hidden_dim_1, hidden_dim_2, hidden_dim_3, out_channels)
    print(model)
    logging.info(model)
    return model

def build_optimizer(model, lr):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    return optimizer
    
def main():
    run = wandb.init()

    # note that we define values from `wandb.config`  
    # instead of defining hard values
    lr  =  wandb.config.lr
    bs = wandb.config.batch_size
    epochs = wandb.config.epochs
    in_channels = wandb.config.in_channels
    hidden_dim_1 = wandb.config.hidden_dim_1
    hidden_dim_2 = wandb.config.hidden_dim_2
    hidden_dim_3 = wandb.config.hidden_dim_3
    out_channels = wandb.config.out_channels
    criterion = wandb.config.criterion
    
    logging.basicConfig(filename = model_name+'.log',
                    level = logging.INFO,
                    format = '%(asctime)s:%(levelname)s:%(message)s')
 
    logging.info(sweep_configuration)
    
    # Prepare data
    test_loader, train_loader, val_loader = data(bs)
    
    # Build gnn model
    model = build_model(in_channels, hidden_dim_1, hidden_dim_2, hidden_dim_3, out_channels)
    model.to(device)
    # Build optimizer
    optimizer = build_optimizer(model, lr)
    
    # Start training and validation process
    min_valid_loss = np.inf
    loss_values = []
    val_loss_values = []
    for epoch in range(epochs):
        train_loss = train_one_epoch(device, model, train_loader, epoch, lr, optimizer)
        #loss_values.append(train_loss)
        val_loss = evaluate_one_epoch(device, model, val_loader, epoch, lr)
        #val_loss_values.append(val_loss)
        wandb.log({
            'epoch': epoch, 
            'train_loss': train_loss, 
            'val_loss': val_loss
        })
# Start sweep job.
wandb.agent(sweep_id, function=main, count=10)
