import torch
import torch.nn.functional as F
from torch.utils.data import random_split
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

import dl
import dl.data
from dl.data import load_hw_digits
import dl.networks
import dl.models


torch.manual_seed(0)
params = {
    'dim': 2,
    'width': 50,
    'depth': 3,
    'lr': 0.01,
    'epochs': 25,
    'batch_size': 10,
    'train_prc': 0.8,
}

# Hand Written Digits dataset
hw_digits_demo = load_digits()

# First let's see what are the different attributes contained in this dataset
print(hw_digits_demo.keys())

# description of the dataset
# print(hw_digits_demo['DESCR']) #commented out, too long (works better for notebook)

# We can see that data and targets are in form of a numpy array 
print(f'type of target: {type(hw_digits_demo["target"])}')
print(f'type of images: {type(hw_digits_demo["images"])}')
print(f'type of data: {type(hw_digits_demo["data"])}')


# creating the figure
fig = plt.figure(figsize=(8, 8))

for i in range(9):
    # setting the new subplot at position i+1 of the 3x3 grid
    ax = fig.add_subplot(3, 3, i+1)
    # i-th image
    img = hw_digits_demo['images'][i]
    # i-th target
    label = hw_digits_demo['target'][i]
    
    ax.imshow(img, cmap='gray')
    ax.set_title(f"{label}")
    # removing ticks and x-y labels
    ax.axis("off")
    
plt.show()

# Using the pyTorch based function this time
hw_digits = load_hw_digits()

# Finding the total number of observations in training and testing
# based on train_prc
len_ = len(hw_digits)
num_train = int(len_ * params['train_prc'])
num_test = len_ - num_train

# Splitting the dataset into training and test sets
train_ds, test_ds = random_split(hw_digits, [num_train, num_test])


# Training the model

# Creating data loaders for the training and test sets
train_loader = torch.utils.data.DataLoader(
    train_ds, batch_size=params['batch_size'], shuffle=True)
test_loader = torch.utils.data.DataLoader(
    test_ds, batch_size=params['batch_size'], shuffle=True)

in_dim = hw_digits.data.shape[-1]
out_dim = len(hw_digits.targets.unique())

network = dl.networks.Dense(in_dim, out_dim, width=params['width'], depth=params['depth'])

optimizer = torch.optim.SGD(network.parameters(), lr=params['lr'])

model = dl.models.Model(network, optimizer, F.cross_entropy, params['epochs'])
_, loss = model.fit(train_loader)


# These lists will help us in the next part as well
test_preds = []
test_targets = []
test_loss_total = 0
total_correct = 0

for batch_num, (data, target) in enumerate(test_loader):
    # output (a list of "probabilities" matched to each digit)
    output = model.network(data)
    # probabilities using softmax based on the output
    pred_prob = F.softmax(output, dim=1)
    pred = pred_prob.argmax(dim=1)
    
    batch_loss = F.cross_entropy(output, target)
    num_correct = pred.eq(target.view_as(pred)).sum().item()
    
    print(f"batch number: {batch_num}, loss = {batch_loss}")
    print(f"correctly classified {num_correct} out of 10\n")
    
    test_preds.append(pred)
    test_targets.append(target)
    total_correct += num_correct
    test_loss_total += batch_loss.item()

test_preds = torch.cat(test_preds, dim=0)
test_targets = torch.cat(test_targets, dim=0)

print("average loss for testing set over all batches = ",test_loss_total / (batch_num+1))

print(f"Total correct calssifications: {total_correct} out of {len(test_preds)}")


# Plotting the same data, this time including the model prediction

# Note that I used the same data we used to make the first plot, not the test data
# I figured the question is asking for the same plot 
# since it says move the digit plot to the end

fig = plt.figure(figsize=(10, 10))

for i in range(9):
    # setting the new subplot at position i+1 of the 3x3 grid
    ax = fig.add_subplot(3, 3, i+1)
    # i-th image
    img = hw_digits.images[i]
    # i-th target
    label = hw_digits.targets[i]
    
    # i-th output of the model
    output = model.network(hw_digits.data[i])
    # Probabilities using softmax based on the output
    pred_prob = F.softmax(output, dim=0)
    # i-th prediction
    pred = pred_prob.argmax(dim=0)
    
    ax.imshow(img, cmap='gray')
    # ax.imshow(img)
    ax.set_title(f"True Label: {label}\nPredicted Label: {pred}")
    # removing ticks and x-y labels
    ax.axis("off")
    
plt.show()