import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.nn.init import xavier_uniform, xavier_normal


class ConvClassifier(nn.Module):
    """
    A convolutional classifier model based on PyTorch nn.Modules.

    The architecture is:
    [(Conv -> ReLU)*P -> MaxPool]*(N/P) -> (Linear -> ReLU)*M -> Linear
    """
    def __init__(self, in_size, out_classes, filters, pool_every, hidden_dims):
        """
        :param in_size: Size of input images, e.g. (C,H,W).
        :param out_classes: Number of classes to output in the final layer.
        :param filters: A list of length N containing the number of
            filters in each conv layer.
        :param pool_every: P, the number of conv layers before each max-pool.
        :param hidden_dims: List of of length M containing hidden dimensions of
            each Linear layer (not including the output layer).
        """
        super().__init__()
        self.in_size = in_size
        self.out_classes = out_classes
        self.filters = filters
        self.pool_every = pool_every
        self.hidden_dims = hidden_dims

        self.feature_extractor = self._make_feature_extractor()
        self.classifier = self._make_classifier()
        print(self)
    def _make_feature_extractor(self):
        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        # TODO: Create the feature extractor part of the model:
        # [(Conv -> ReLU)*P -> MaxPool]*(N/P)
        # Use only dimension-preserving 3x3 convolutions (you will need to add padding). Apply 2x2 Max
        # Pooling to reduce dimensions.
        # If P>N you should implement:
        # (Conv -> ReLU)*N
        # Hint: use loop for len(self.filters) and append the layers you need to the list named 'layers'.
        # Use :
        # if <layer index>%self.pool_every==0:
        #     ...
        # in order to append maxpooling layer in the right places.
        # ====== YOUR CODE: ======
        for num_conv in range(len(self.filters)):
            layers.append(nn.Conv2d(in_channels, self.filters[num_conv], 3, padding=1))
            layers.append(nn.ReLU())
            in_channels = self.filters[num_conv]
            if (num_conv + 1) % self.pool_every == 0:
                layers.append(nn.MaxPool2d(2))
        # raise NotImplementedError()
        # ========================
        seq = nn.Sequential(*layers)
        return seq

    def _make_classifier(self):
        in_channels, in_h, in_w = tuple(self.in_size)

        layers = []
        # TODO: Create the classifier part of the model:
        # (Linear -> ReLU)*M -> Linear
        # You'll need to calculate the number of features first.
        # The last Linear layer should have an output dimension of out_classes.
        # Hint: use loop for len(self.hidden_dims) and append the layers you need to list named layers.
        # ====== YOUR CODE: ======
        num_features = self.filters[-1] * (in_h // (2 ** (len(self.filters) // self.pool_every))) * (in_w // (2 ** (len(self.filters) // self.pool_every)))
        for num_hidden in range(len(self.hidden_dims)):
            layers.append(nn.Linear(num_features, self.hidden_dims[num_hidden]))
            layers.append(nn.ReLU())
            num_features = self.hidden_dims[num_hidden]
        layers.append(nn.Linear(num_features, self.out_classes))
        # raise NotImplementedError()
        # ========================
        seq = nn.Sequential(*layers)
        return seq

    def forward(self, x):
        # TODO: Implement the forward pass.
        # Extract features from the input (using self.feature_extractor), flatten your result (using torch.flatten),
        # run the classifier on them (using self.classifier) and return class scores.
        # ====== YOUR CODE: ======
        x = self.feature_extractor(x)
        x = torch.flatten(x, 1)
        out = self.classifier(x)
        # raise NotImplementedError()
        # ========================
        return out


class YourCodeNet(ConvClassifier):
    def __init__(self, in_size, out_classes, filters, pool_every, hidden_dims):
        super().__init__(in_size, out_classes, filters, pool_every, hidden_dims)

    # TODO: Change whatever you want about the ConvClassifier to try to
    # improve it's results on CIFAR-10.
    # For example, add batchnorm, dropout, skip connections, change conv
    # filter sizes etc.
    # ====== YOUR CODE: ======
    def _make_feature_extractor(self):
        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        # Implement this function with the fixes you suggested question 1.1. Extra points.
        # ====== YOUR CODE: ======
        for num_conv in range(len(self.filters)):
            layers.append(nn.Conv2d(in_channels, self.filters[num_conv], 3, padding=1))
            layers.append(nn.ReLU())
            #layers.append(nn.Dropout2d(0.2))
            #layers.append(nn.BatchNorm2d(self.filters[num_conv])) # added after we were asked to add batchnorm
            in_channels = self.filters[num_conv]
            if (num_conv + 1) % self.pool_every == 0:
                layers.append(nn.MaxPool2d(2))
        # raise NotImplementedError()
        # ========================
        seq = nn.Sequential(*layers)
        return seq
    # ========================

