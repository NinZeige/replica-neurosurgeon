from torchvision import models
from torch import nn
from . import AlexNet

def squeeze_vgg(vgg: models.VGG) -> nn.Module:
    return AlexNet.squeeze_alex(vgg)

def flatten_vgg() -> nn.Module:
    vgg = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
    return squeeze_vgg(vgg)