# Imports
import torch
import torch.nn as nn  # All neural network modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim  # For all Optimization algorithms, SGD, Adam, etc.
import torchvision.transforms as transforms  # Transformations we can perform on our dataset
import torchvision
import os
import pandas as pd
from tqdm import tqdm
from skimage import io
from skimage.transform import rescale, resize, downscale_local_mean
from torch.utils.data import (
    Dataset,
    DataLoader,
)  # Gives easier dataset managment and creates mini batches
from sklearn import metrics


class ImagesDataProcess(Dataset):
    def __init__(self,csv_file,root_dir,tranform=None):
        self.annotation=pd.read_csv(csv_file)
        self.root_dir=root_dir
        self.tranform=tranform
        
    def __len__(self):
        return len(self.annotation)
    
    def __getitem__(self,index):
        img_path=os.path.join(self.root_dir,self.annotation.iloc[index,0])
        image=io.imread(img_path)
        image=resize(image,(250,250),anti_aliasing=True)
        y_label=torch.tensor(int(self.annotation.iloc[index,1]))
        
        if self.tranform:
            image=self.tranform(image)
        return (image,y_label)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters
in_channel = 3
num_classes = 3
learning_rate = 1e-3
batch_size = 32
num_epochs = 3
#root_dir_path='../input/cat-dog-images-for-classification/cat_dog'
root_dir_path="dataset"
#csv_file_path='../input/cat-dog-imagEes-for-classification/cat_dog.csv'
csv_file_path="us_GA.csv"

dataset=ImagesDataProcess(
    csv_file=csv_file_path,
    root_dir=root_dir_path,
    tranform=transforms.ToTensor()
)

len(dataset)

train_set, test_set = torch.utils.data.random_split(dataset, [468, 117])
train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

# Model
model = torchvision.models.googlenet(pretrained=True)
model.fc=nn.Sequential(
    nn.Linear(in_features=1024,out_features=512),
    nn.ReLU(),
    nn.Linear(in_features=512,out_features=128),
    nn.ReLU(),
    nn.Linear(in_features=128,out_features=32),
    nn.ReLU(),
    nn.Linear(in_features=32,out_features=3,bias=True)
) 
model.to(device)

from torchsummary import summary

print(summary(model, (3, 250, 250),verbose=0))

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train Network
for epoch in range(num_epochs):
    losses = []

    for batch_idx, (data, targets) in tqdm(enumerate(train_loader)):
        # Get data to cuda if possible
        data = data.to(device=device,dtype=torch.float)
        targets = targets.to(device=device)

        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        losses.append(loss.item())

        # backward
        optimizer.zero_grad()
        loss.backward()

        # gradient descent or adam step
        optimizer.step()

    print(f"Cost at epoch {epoch} is {sum(losses)/len(losses)}")

# Check accuracy on training to see how good our model is
def check_accuracy(loader, model):
    num_correct = 0
    num_samples = 0
    model.eval()

    with torch.no_grad():
        for x, y in tqdm(loader):
            x = x.to(device=device, dtype=torch.float)
            y = y.to(device=device)

            scores = model(x)
            _, predictions = scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)

        # matrix = metrics.confusion_matrix(predictions.detach().cpu().numpy(), y.detach().cpu().numpy())
        # print(matrix.diagonal()/matrix.sum(axis=1))

        print(
            f"Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}"
        )

    model.train()

print("Checking accuracy on Training Set")
check_accuracy(train_loader, model)

print("Checking accuracy on Test Set")
check_accuracy(test_loader, model)

