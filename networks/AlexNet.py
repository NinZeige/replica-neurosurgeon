from torchvision import models
import torch
from torch import nn

def squeeze_alex(alex: models.AlexNet) -> nn.Module:
    flatten_alex = nn.Module()
    numbering = 1
    def unwrap(modu: nn.Module) -> None:
        nonlocal numbering  # Avoid UnboundLocalError
        for layers in modu.children():
            flatten_alex.add_module(f'{numbering}--{layers.__class__.__name__}', layers)
            numbering += 1
    unwrap(alex.features)
    unwrap(alex.avgpool)
    flt_layer = nn.Flatten()
    flatten_alex.add_module(f'{numbering}--{flt_layer.__class__.__name__}', flt_layer)
    numbering += 1
    unwrap(alex.classifier)
    return flatten_alex


def flatten_alex() -> nn.Module:
    alex = models.alexnet(weights=models.AlexNet_Weights.DEFAULT)
    return squeeze_alex(alex)