from __future__ import print_function
import torch
import torch.nn as nn
from torch.nn import functional as F


class Encoder(nn.Module):
    def __init__(self, in_channels, latent_size, d=128):
        super(Encoder, self).__init__()
        self.in_channels = in_channels
        self.latent_size = latent_size
        self.d = d

        self.conv1_1 = nn.Conv2d(self.in_channels, self.d // 2, 4, 2, 1)
        self.conv2 = nn.Conv2d(self.d // 2, self.d * 2, 4, 2, 1)
        self.conv2_bn = nn.BatchNorm2d(self.d * 2)
        self.conv3 = nn.Conv2d(self.d * 2, self.d * 4, 4, 2, 1)
        self.conv3_bn = nn.BatchNorm2d(self.d * 4)
        self.conv4 = nn.Conv2d(self.d * 4, self.latent_size, 4, 1, 0)

    def forward(self, x):
        x = F.leaky_relu(self.conv1_1(x), 0.2)
        x = F.leaky_relu(self.conv2_bn(self.conv2(x)), 0.2)
        x = F.leaky_relu(self.conv3_bn(self.conv3(x)), 0.2)
        x = self.conv4(x)
        return torch.tanh(x)


class Generator(nn.Module):
    def __init__(self, in_channels, latent_size, d=128):
        super(Generator, self).__init__()
        self.in_channels = in_channels
        self.latent_size = latent_size
        self.d = d

        self.deconv1_1 = nn.ConvTranspose2d(self.latent_size, self.d * 2, 4, 1, 0)
        self.deconv1_1_bn = nn.BatchNorm2d(self.d * 2)
        self.deconv1_2 = nn.ConvTranspose2d(10, self.d * 2, 4, 1, 0)
        self.deconv1_2_bn = nn.BatchNorm2d(self.d * 2)
        self.deconv2 = nn.ConvTranspose2d(self.d * 2, self.d * 2, 4, 2, 1)
        self.deconv2_bn = nn.BatchNorm2d(self.d * 2)
        self.deconv3 = nn.ConvTranspose2d(self.d * 2, self.d, 4, 2, 1)
        self.deconv3_bn = nn.BatchNorm2d(self.d)
        self.deconv4 = nn.ConvTranspose2d(self.d, self.in_channels, 4, 2, 1)

    # forward method
    def forward(self, x):
        x = F.relu(self.deconv1_1_bn(self.deconv1_1(x)))
        x = F.relu(self.deconv2_bn(self.deconv2(x)))
        x = F.relu(self.deconv3_bn(self.deconv3(x)))
        x = F.tanh(self.deconv4(x)) * 0.5 + 0.5
        return x


class Discriminator(nn.Module):
    def __init__(self, latent_size, d=128):
        super(Discriminator, self).__init__()
        self.latent_size = latent_size
        self.d = d

        self.linear1 = nn.Linear(self.latent_size, self.d)
        self.linear2 = nn.Linear(self.d, self.d)
        self.linear3 = nn.Linear(self.d, 1)

    def forward(self, x):
        x = F.leaky_relu((self.linear1(x)), 0.2)
        x = F.leaky_relu((self.linear2(x)), 0.2)
        x = torch.sigmoid(self.linear3(x))
        return x


class MNIST_Encoder(nn.Module):
    def __init__(self, in_channels, latent_size):
        super(MNIST_Encoder, self).__init__()
        self.in_channels = in_channels
        self.latent_size = latent_size

        self.linear1 = nn.Linear(self.in_channels, self.latent_size)
        self.linear2 = nn.Linear(self.latent_size, self.latent_size)

    def forward(self, x):
        x = F.leaky_relu((self.linear1(x)), 0.2)
        x = torch.tanh((self.linear2(x)))
        return x


class MNIST_Generator(nn.Module):
    def __init__(self, out_channels, latent_size):
        super(MNIST_Generator, self).__init__()
        self.out_channels = out_channels
        self.latent_size = latent_size

        self.linear1 = nn.Linear(self.latent_size, self.out_channels)
        self.linear2 = nn.Linear(self.out_channels, self.out_channels)

    def forward(self, x):
        x = F.leaky_relu((self.linear1(x)), 0.2)
        x = F.leaky_relu((self.linear2(x)), 0.2)
        return x


class MNIST_Discriminator(nn.Module):
    def __init__(self, latent_size):
        super(MNIST_Discriminator, self).__init__()
        self.latent_size = latent_size

        self.linear1 = nn.Linear(self.latent_size, self.latent_size // 2)
        self.linear2 = nn.Linear(self.latent_size // 2, 1)

    def forward(self, x):
        x = F.leaky_relu((self.linear1(x)), 0.2)
        x = torch.sigmoid(self.linear2(x))
        return x
