from tensorflow.keras.datasets import fashion_mnist
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score

#importing the data from tensorflow
(pixels_tensor, labels_tensor), (X_test, Y_test) = fashion_mnist.load_data()

#randomly selecting 5000 from the set of 60000 images
random_indices = np.random.choice(pixels_tensor.shape[0], 5000, replace=False)
pixels_tensor = pixels_tensor[random_indices]
labels_tensor = labels_tensor[random_indices]

del X_test, Y_test

pixels = pixels_tensor.reshape(pixels_tensor.shape[0], -1)

# Convert the images into a DataFrame
pixels = pd.DataFrame(pixels)

# Convert the labels into a Series
labels = pd.Series(labels_tensor, name="label")

# Concatenate the labels and images data
df = pd.concat([labels, pixels], axis=1)

#%% 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

kmeans = KMeans(n_clusters=10, random_state=0, n_init = 'auto').fit(pixels)
clusters = kmeans.labels_

# Mapping cluster labels to original labels
mapping = dict()

# Iterate through each cluster
for i in range(10):
    indices = np.where(clusters == i)
    cluster_labels = labels_tensor[indices]
    most_common_label = np.argmax(np.bincount(cluster_labels))
    mapping[i] = most_common_label

# Display the mapping
print("Cluster to label mapping:", mapping)

fig, ax = plt.subplots(2, 5, figsize=(28, 12))
centers = kmeans.cluster_centers_.reshape(10, 28, 28)
for i, (axi, center) in enumerate(zip(ax.flat, centers)):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)
    axi.set_title(f"Cluster {i} - Label {mapping[i]}")
    
# Compute WCSS
wcss = kmeans.inertia_
print(f"WCSS: {wcss}")

# Compute Silhouette Coefficient
silhouette_coefficient = silhouette_score(pixels, clusters)
print(f"Silhouette Coefficient: {silhouette_coefficient}")


del fig, ax, centers, center, axi, clusters, mapping, cluster_labels, i, indices, most_common_label

#%%
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Normalizing the data
pixels_tensor = pixels_tensor / 255.0

# Create a TensorDataset
train_dataset = TensorDataset(torch.FloatTensor(pixels_tensor), torch.LongTensor(labels_tensor))

# Create a DataLoader
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.5),
        )
        self.decoder = nn.Sequential(
            nn.Linear(64, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.5),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Instantiate the model, loss, and optimizer
model = Autoencoder()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model
num_epochs = 50
for epoch in range(num_epochs):
    epoch_loss = 0
    num_batches = 0
    
    for data, _ in train_loader:
        data = data.view(data.size(0), -1)
        output = model(data)
        loss = criterion(output, data)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        num_batches += 1

    avg_loss = epoch_loss / num_batches
    print(f"Epoch [{epoch + 1}/{num_epochs}], Avg Loss: {avg_loss}")

# Obtain the latent representations
with torch.no_grad():
    latent_vectors = []
    for data, _ in train_loader:
        data = data.view(data.size(0), -1)
        latent_vectors.append(model.encoder(data))

latent_vectors = torch.cat(latent_vectors, dim=0)
latent_vectors = latent_vectors.numpy()

# Perform KMeans clustering on the latent representations
kmeans = KMeans(n_clusters=10, random_state=0).fit(latent_vectors)
clusters = kmeans.labels_

# Mapping cluster labels to original labels
mapping = dict()

for i in range(10):
    indices = np.where(clusters == i)
    cluster_labels = labels_tensor[indices]
    most_common_label = np.argmax(np.bincount(cluster_labels))
    mapping[i] = most_common_label

print("Cluster to label mapping:", mapping)

# Visualize cluster centers as images
fig, ax = plt.subplots(2, 5, figsize=(28, 12))
centers = kmeans.cluster_centers_.reshape(10, 8, 8)
for i, (axi, center) in enumerate(zip(ax.flat, centers)):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)
    axi.set_title(f"Cluster {i} - Label {mapping[i]}")

plt.show


#%%
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Normalizing the data
pixels_tensor = pixels_tensor / 255.0

# Create a TensorDataset
train_dataset = TensorDataset(torch.FloatTensor(pixels_tensor), torch.LongTensor(labels_tensor))

# Create a DataLoader
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.5),
        )
        self.decoder = nn.Sequential(
            nn.Linear(64, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


# Instantiate the model, loss, and optimizer
model = Autoencoder()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model
num_epochs = 50
for epoch in range(num_epochs):
    for data, _ in train_loader:
        data = data.view(data.size(0), -1)
        output = model(data)
        loss = criterion(output, data)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}")

# Obtain the latent representations
with torch.no_grad():
    latent_vectors = []
    for data, _ in train_loader:
        data = data.view(data.size(0), -1)
        latent_vectors.append(model.encoder(data))

latent_vectors = torch.cat(latent_vectors, dim=0)
latent_vectors = latent_vectors.numpy()

# Perform KMeans clustering on the latent representations
kmeans = KMeans(n_clusters=10, random_state=0).fit(latent_vectors)
clusters = kmeans.labels_

# Mapping cluster labels to original labels
mapping = dict()

for i in range(10):
    indices = np.where(clusters == i)
    cluster_labels = labels_tensor[indices]
    most_common_label = np.argmax(np.bincount(cluster_labels))
    mapping[i] = most_common_label

print("Cluster to label mapping:", mapping)

# Compute WCSS
wcss = kmeans.inertia_
print(f"WCSS: {wcss}")

# Compute Silhouette Coefficient
silhouette_coefficient = silhouette_score(latent_vectors, clusters)
print(f"Silhouette Coefficient: {silhouette_coefficient}")


# Visualize cluster centers as images
fig, ax = plt.subplots(2, 5, figsize=(28, 12))
centers = kmeans.cluster_centers_.reshape(10, 8, 8)
for i, (axi, center) in enumerate(zip(ax.flat, centers)):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)
    axi.set_title(f"Cluster {i} - Label {mapping[i]}")

plt.show