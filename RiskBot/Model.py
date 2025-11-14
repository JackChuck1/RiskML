import torch
import torch.nn as nn

class PlaceModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(42, 42),
            nn.ReLU(),
            nn.Linear(42, 42),
            nn.ReLU(),
            nn.Linear(42, 42),
        )

    def forward(self, x):
        outputs = self.linear_relu_stack(x)
        return outputs

class AttackModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(42, 84),
            nn.ReLU(),
            nn.Linear(84, 84),
            nn.ReLU(),
            nn.Linear(84, 84),
        )

    def forward(self, x):
        outputs = self.linear_relu_stack(x)
        return outputs