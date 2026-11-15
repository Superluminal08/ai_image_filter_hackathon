import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import torchvision.transforms as transforms
import numpy as np
import os
from sklearn.model_selection import train_test_split
import torch.nn as nn
import torch
import torch.optim as optim
import torch.nn.functional as F
from PIL import Image
from sklearn.metrics import precision_score, recall_score, f1_score
import os
import requests
from io import BytesIO
image_size = 32
class ImageClassifier(nn.Module):
    def __init__(self, num_classes, input_size=(image_size, image_size), channels = 3):
        super(ImageClassifier, self).__init__()

        self.input_size = input_size
        self.channels = channels
        self.conv1 = nn.Conv2d(channels, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(256)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        self._to_linear = None
        self._calculate_to_linear(input_size)
        self.fc1 = nn.Linear(self._to_linear, 512)
        self.fc2 = nn.Linear(512, num_classes)
    def _calculate_to_linear(self, input_size):
        x = torch.randn(1, self.channels, *input_size)
        self.conv_forward(x)
    def conv_forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        if self._to_linear is None:#
            self._to_linear = x[0].shape[0] * x[0].shape[1] * x[0].shape[2]
        return x
    def forward(self, x):
        x = self.conv_forward(x)
        x = x.view(-1, self._to_linear)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class_names = ["FAKE", "REAL"]
def Check(url):
    ##load model
    model = ImageClassifier(num_classes=2, input_size=(image_size, image_size))
    model.load_state_dict(torch.load("classifier.pth"))
    model.eval()

    #load from url
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except:
        print (f"failed to load image at: {url}")
        return


    img = Image.open(BytesIO(response.content))
    
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor()
    ])
    image_tensor = transform(img).unsqueeze(0)

    ##make prediction
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        prediction = class_names[predicted.item()]
        return prediction

