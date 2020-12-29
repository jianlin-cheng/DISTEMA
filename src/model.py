"""
@ Description: Deep Learning model
@ Author: Shawn Chen
@ Create date: 2020-12-29
"""

import os
import sys
import time
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F


class GlobalMaxPool2d(nn.Module):
    def __init__(self):
        super(GlobalMaxPool2d, self).__init__()
    def forward(self, x):
        return F.max_pool2d(x, kernel_size=x.size()[2:])


class SELayer(nn.Module):
    def __init__(self, channel, reduction=8):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )
    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class mynet(nn.Module):
    def __init__(self):
        super(mynet, self).__init__()
        
        self.c1 = nn.Conv2d(1, 96, kernel_size=5, stride=2, padding=1)
        self.b1 = nn.BatchNorm2d(96)
        self.m1 = nn.MaxPool2d(kernel_size=3, stride=2)

        self.c2 = nn.Conv2d(96, 256, kernel_size=5, padding=2)
        self.b2 = nn.BatchNorm2d(256)
        self.m2 = nn.MaxPool2d(kernel_size=3, stride=2)
        
        self.c3 = nn.Conv2d(256, 384, kernel_size=3, padding=1)
        self.b3 = nn.BatchNorm2d(384)

        self.c4 = nn.Conv2d(384, 256, kernel_size=3, padding=1)
        self.b4 = nn.BatchNorm2d(256)
        self.m4 = nn.MaxPool2d(kernel_size=3, stride=2)

        self.selayer_1 = SELayer(96)
        self.selayer_2 = SELayer(256)

        self.gm = GlobalMaxPool2d()
        
        self.fc = nn.Flatten()

        self.ds1 = nn.Linear(256, 128)
        self.dp1 = nn.Dropout()
        
        self.ds2 = nn.Linear(128, 64)
        self.dp2 = nn.Dropout()
        
        self.ds3 = nn.Linear(64, 32)
        self.dp3 = nn.Dropout()

        self.ds4 = nn.Linear(32, 1)

    def forward(self, x):
        l1 = self.b1(self.c1(x))
        l1 = self.selayer_1(l1)
        l1 = self.m1(F.leaky_relu(l1))
    
        l2 = self.b2(self.c2(l1))
        l2 = self.selayer_2(l2)
        l2 = self.m2(F.leaky_relu(l2))

        l3 = self.b3(self.c3(l2))
        l3 = F.leaky_relu(l3)

        l4 = self.b4(self.c4(l3))
        l4 = self.m4(F.leaky_relu(l4))        
        
        l5 = self.gm(l4)
        
        l6 = self.fc(l5)
        
        l7 = self.dp1(F.leaky_relu(self.ds1(l6)))
        l8 = self.dp2(F.leaky_relu(self.ds2(l7)))
        l9 = self.dp3(F.leaky_relu(self.ds3(l8)))
        l10 = F.relu(self.ds4(l9))           
        
        return l10