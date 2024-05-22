#paso 1 instala todas las librerias necesarias
import os
import torch
from ultralytics import YOLO
from datasets import load_dataset
import torchvision.datasets as datasets

import torchvision.transforms as transforms
#paso 2 descarga el dataset
#data =load_dataset("fashion_mnist")

"""
pase 3 despues de descargarlas ponemos la data set
en un formato que pueda leer el modelo de Yolo seccionandolo en carpetas
"""

"""
validation_set = datasets.FashionMNIST(
    root="datasets",
    train=False,
    download=True,
    transform=transforms
)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485], std=[0.229])
])

def prepocessing(partition: str, data: object):
    os.makedirs(f"datasets/images/{partition}", exist_ok=True)
    os.makedirs(f"datasets/labels/{partition}", exist_ok=True)

    for i,sample in enumerate(data[partition]):
        img = sample["image"]
        label = sample["label"]

        img = transform(img)

        with open(f"datasets/labels/{partition}/{i}.txt", "w") as f:
            f.write(f"{label}\n")
        torch.save(img, f"datasets/images/{partition}/{i}.png")

if __name__=='__main__':
    data = load_dataset("fashion_mnist")

    prepocessing("train",data)
    prepocessing("test",data)
    prepocessing("validation",data)    
    
"""
#instala y entrena el modelo Yolov8 con la dataset anterior   

# Define the path to the dataset YAML file
yaml_path = "train.yaml"

# Define the path to the pretrained weights
weights_path = "yolov8l.pt"

# Define the number of epochs for training
epochs = 5

# Load the YOLOv8 model
model = YOLO(weights_path)

# Train the model
results = model.train(data=yaml_path, epochs=epochs)

# Save the trained model
torch.save(model.state_dict(), "yolov8_fashion_mnist.pt")


