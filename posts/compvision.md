---
title: Computer Vision Algorithm
categories: [web, resources]
date: 09-05-2024
draft: true
---


## feature extraction

```python
import os

import numpy as np

import torch

import torch.nn as nn

from torchvision import models

from torchvision.models import EfficientNet_B0_Weights

import pandas as pd

from PIL import Image

import time

  

def read_file_list(filename):

    file = open(filename)

    data = file.read()

    lines = data.replace(",", " ").replace("\t", " ").split("\n")

    list = [[v.strip() for v in line.split(" ") if v.strip() != ""] for line in lines if len(line) > 0 and line[0] != "#"]

    list = [(float(l[0]), l[1:]) for l in list if len(l) > 1]

    return dict(list)

  

class FeatureExtractor(nn.Module):

    def __init__(self):

        super(FeatureExtractor, self).__init__()

        self.efficientnet = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)

        # Modify first layer to accept 6 channels (RGB + Depth)

        original_layer = self.efficientnet.features[0][0]

        self.efficientnet.features[0][0] = nn.Conv2d(6, 32, kernel_size=3, stride=2, padding=1, bias=False)

        # Initialize weights for the new channels

        with torch.no_grad():

            new_weights = torch.zeros_like(self.efficientnet.features[0][0].weight)

            new_weights[:, :3, :, :] = original_layer.weight

            new_weights[:, 3:, :, :] = original_layer.weight

            self.efficientnet.features[0][0].weight = nn.Parameter(new_weights)

        # Remove the classifier head

        self.efficientnet.classifier = nn.Identity()

  

        # Add AdaptiveAvgPool2d to get a 1x1 feature map

        self.adaptive_pool = nn.AdaptiveAvgPool2d((1, 1))

  

        # Time tracking

        self.forward_time = 0

        self.forward_count = 0

  

    def forward(self, x):

        start_time = time.time()

        features = self.efficientnet.features(x)

        features = self.adaptive_pool(features) # Pool to 1x1

        features = features.flatten(start_dim=1)  # Flatten to get the feature vector

        end_time = time.time()

        self.forward_time += (end_time - start_time)

        self.forward_count += 1

        return features

  

class Dataset:

    def __init__(self, base_dir, transform=None):

        self.base_dir = base_dir

        self.transform = transform

  

        self.rgb_dict = read_file_list(os.path.join(base_dir, 'rgb.txt'))

        self.depth_dict = read_file_list(os.path.join(base_dir, 'depth.txt'))

        self.groundtruth = pd.read_csv(os.path.join(base_dir, 'groundtruth.txt'),

                                    sep=' ', comment='#', header=None,

                                    names=['timestamp', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw'])

  

        self.rgb_timestamps = list(self.rgb_dict.keys())

        self.depth_timestamps = list(self.depth_dict.keys())

        self.synced_timestamps = self.synchronize_timestamps()

  

    def synchronize_timestamps(self):

        synced = []

        for rgb_time in self.rgb_timestamps:

            depth_time = min(self.depth_timestamps, key=lambda x: abs(x - rgb_time))

            if abs(rgb_time - depth_time) < 0.02:

                synced.append((rgb_time, depth_time))

        return synced

  

    def __len__(self):

        return len(self.synced_timestamps)

  

    def __getitem__(self, idx):

        rgb_time, depth_time = self.synced_timestamps[idx]

  

        rgb_path = os.path.join(self.base_dir, self.rgb_dict[rgb_time][0])

        depth_path = os.path.join(self.base_dir, self.depth_dict[depth_time][0])

  

        rgb_img = Image.open(rgb_path).convert('RGB')

        depth_img = Image.open(depth_path).convert('RGB')

  

        if self.transform:

            rgb_img = self.transform(rgb_img)

            depth_img = self.transform(depth_img)

  

        closest_gt = self.groundtruth.iloc[(self.groundtruth['timestamp'] - rgb_time).abs().argsort()[0]]

        pose = closest_gt[['tx', 'ty', 'tz']].values.astype(np.float32)

  

        return rgb_img, depth_img, torch.tensor(pose)

  

        pass

  

def main():

    # Example usage of feature extractor

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    feature_extractor = FeatureExtractor().to(device)

    # Example dummy input

    dummy_input = torch.randn(1, 6, 224, 224).to(device)

    features = feature_extractor(dummy_input)

    print(f"Feature shape: {features.shape}")

  

if __name__ == "__main__":

    main()
```

- **Understanding the Output Shape:**

- **torch.Size:** This part simply tells you that the output is a PyTorch tensor, which is a multi-dimensional array specifically designed for numerical operations in PyTorch (and deep learning in general).

- [1, 1280] This is the actual shape of your tensor, and it represents the dimensions of the array:

  - **1 (First Dimension):** This represents the batch size. In your case, you are passing a single example image or a batch size of 1. If you were processing multiple images at once (common in training), this number would be the number of images in your batch.

    - **1280 (Second Dimension):** This is the exciting part! This is the dimensionality of the extracted feature vector. Each of the 1280 numbers represents a specific, learned feature extracted from the input image by EfficientNet-B0.

**What are these 1280 features?**

- **Learned Representations:** These features are not human-interpretable things like "color = blue" or "shape = round." Instead, they are complex, abstract representations of the image learned by the EfficientNet model during its training on a massive dataset (probably ImageNet).

- **Meaning in Context:** The meaning of these features is only relevant in the context of the task you want to solve:

  - **Image Classification:** If you use these features for classification, a classifier (like a linear layer) will learn to map combinations of these 1280 features to specific image categories (e.g., "cat," "dog," "car").

  - **VSLAM:** In your VSLAM system, these features might be used to identify similar areas or landmarks in different images, helping to estimate the camera's position and build a map.

**Analogy:**

Imagine you are describing a cake to someone. Instead of saying "it's brown and round," you provide them with 1280 data points representing:  

- Texture measurements at different points  
- Sweetness levels of different layers  
- Ingredient composition analysis

These data points are the "features." They might not directly tell the person what the cake looks like, but they contain rich information that can be used to identify, classify, or compare cakes.

**Key Takeaway:** The torch.Size([1, 1280]) output means your FeatureExtractor is successfully producing a 1280-dimensional feature vector for each image you input. The meaning of these features is dependent on how you use them in your downstream tasks (classification, VSLAM, etc.).

## object_classification.py
