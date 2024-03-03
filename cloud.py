import torch
from torch import nn
import json
from torchvision import models

CATOGARY = './imagenet_classes.json'
INPUT_TENSOR = '/tmp/input.tensor'

def cloud_main():
    alex = models.alexnet(pretrained=True)
    alex.eval()
    with open(INPUT_TENSOR, 'rb') as f:
        medium:torch.Tensor = torch.load(f)
        medium = alex.avgpool(medium)
        flatten = nn.Flatten()
        medium = flatten(medium)
        medium = alex.classifier(medium)
    # read category
    with open(CATOGARY, 'r') as f:
        cate = json.load(f)
        reinter = lambda x: [cate[f'{index}'] for index in x]
    
    _, top5 = torch.topk(medium, 5)
    print(reinter(top5[0]))

if __name__ == '__main__':
    cloud_main()