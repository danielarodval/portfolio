#%% Part 1
import torch
import numpy as np

def f(x,y):
    return (torch.sin(x)**3 - torch.sin(y)**3)/(3*x**2 + 5*y**2)

x = torch.linspace(-5, 5, 100)
y = torch.linspace(-5, 5, 100)
X, Y = torch.meshgrid(x, y, indexing='ij')

#%% Part 2
z = f(x,y)
za = z.numpy()

print(f"tensor z shape: {z.shape}")
print(f"numpy export shape: {za.shape}")

print(f"\ntensor z axes/dimensions: {z.ndim}")
print(f"numpy export axes/dimensions: {za.ndim}")

print(f"\ntensor z total number of entries: {z.numel()}")
print(f"numpy export total number of entries: {za.size}")

#%% Part 3
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.concatenate((a, b))
print(f"\nnumpy concatenated arrays: {c}")

t1 = torch.tensor([1, 2, 3])
t2 = torch.tensor([4, 5, 6])
t3 = torch.cat((t1, t2))
print(f"\npytorch concatenated tensors: {t3}")