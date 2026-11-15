print ("Beginning imports")

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
import random

print ("Imported all")
def LoadDataset():
    classes = []
    paths = os.listdir("C:\\Users\\camer\\Desktop\\Datasets\\ai image dataset\\train\\ALL")
    for path in paths:
        if "FAKE" in path:
            classes.append("FAKE")
        else:
            classes.append("REAL")
    return (paths, classes)


def GetRandomDataset(dataset, size): ##recieves dataset of labels and images as tuple
    labels = []
    images = []
    for i in range(size):
        index = random.randint(0, len(dataset[0]))
        labels.append(dataset[1][index])
        images.append(dataset[0][index])
    return (images, labels)

class TrainingData(Dataset):
    def __init__(self, csv_df, class_list, transform=None):
        self.df = csv_df
        self.transform = transform
        self.class_list = class_list
    def __len__(self):
        return self.df.shape[0]
    def __getitem__(self, index):
        img_dir = "C:\\Users\\camer\\Desktop\\Datasets\\ai image dataset\\train\\ALL\\"
        try:
            image_path = img_dir + self.df.iloc[index]["image"]
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            return self.__getitem__((index + 1) % len(self.df)) 
        label = self.class_list.index(self.df.iloc[index]["label"])
        if self.transform:
            image = self.transform(image)
        return image, label
class EarlyStopping:
    def __init__(self, patience=3, delta=0):
        self.counter = 0
        self.best_model_state = None
        self.patience = patience
        self.delta = delta
        self.best_score = None
        self.early_stop = False
    def __call__(self, val_loss, model):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.best_model_state = model.state_dict()
        elif score < self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.best_model_state = model.state_dict()
            self.counter = 0
    def load_best_model(self, model):
        model.load_state_dict(self.best_model_state)



print ("Beginning")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

class_list = ["FAKE", "REAL"]
image_list , label_list = GetRandomDataset(LoadDataset(), 100)

df = pd.DataFrame()
df["image"] = image_list
df["label"] = label_list

test_ratio = 0.2
train_df, test_df = train_test_split(df, test_size=test_ratio, stratify=df["label"])

image_size = 32
training_transform = transforms.Compose([transforms.Resize((image_size, image_size)), 
                                         transforms.RandomRotation(10),
                                         transforms.ToTensor()])
test_transforms = transforms.Compose([transforms.Resize((image_size, image_size)),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

batch_size = 10
train_data_object = TrainingData(train_df, class_list, training_transform)

test_data_object = TrainingData(test_df, class_list, test_transforms)

train_loader = DataLoader(train_data_object, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data_object, batch_size=batch_size, shuffle=False)

print ("Loaded and processed training data")

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




epochs = 100
learning_rate = 0.001
num_classes = len(class_list)
input_size = (image_size, image_size)
channels = 3
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ImageClassifier(num_classes, input_size, channels).to(device)

criterion = nn.CrossEntropyLoss()
optimiser = optim.Adam(model.parameters(), lr=learning_rate)
early_stopping = EarlyStopping(patience=3)

#training loop
print ("Beginning training loop")
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        optimiser.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimiser.step()
        running_loss += loss.item()
    print (f'Epoch [{epoch + 1} / {epochs}], Loss: {running_loss/len(train_loader):.4f}')
    #validate
    model.eval()
    all_predictions = []
    all_labels = []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
        early_stopping(running_loss, model)
        if early_stopping.early_stop:
            print ("Stopping early")
            break
    early_stopping.load_best_model(model)
    #metrics
    accuracy = 100 * sum(np.array(all_predictions) == np.array(all_labels)) / len(all_labels)
    precision = precision_score(all_labels, all_predictions, average="weighted")
    recall = recall_score(all_labels, all_predictions, average="weighted")
    f1 = f1_score(all_labels, all_predictions, average="weighted")
    print (f"Epoch [{epoch+1}/{epochs}]")
    print (f"Test Accuracy: {accuracy:.2f}%")
    print (f"Precision: {precision:.4f}")
    print (f"Recall: {recall:.4f}")
    print (f"F1 Score: {f1:.4f}")
print ("Finished training")

#save model
torch.save(model.state_dict(), 'classifier.pth')