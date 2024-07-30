import numpy as np
import time
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch import nn
from torch import optim


class HAR(nn.Module):
    def __init__(self):
        super(HAR, self).__init__()

        # image as input

        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        x = self.pool(nn.ReLU(self.conv1(x)))
        x = self.pool(nn.ReLU(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = nn.ReLU(self.fc1(x))
        x = nn.ReLU(self.fc2(x))
        x = self.fc3(x)
        return x



## main

if __name__ == "__main__":
    # create an array of (256,256,3) image

    image = np.random.rand(256,256,3)

    # create a model

    model = HAR()

# create a tensor from the image

    image_tensor = torch.tensor(image, dtype=torch.float32)

    print(image_tensor.shape)

    # forward pass the image tensor through the model

    output = model(image_tensor)

    print(output.shape)


