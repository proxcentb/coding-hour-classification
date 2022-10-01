import torch.nn as nn

class Net(nn.Module):
    def __init__(self, out_features):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=7, padding=3, bias=False, padding_mode='zeros')
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=5, padding=2, bias=False, padding_mode='zeros')
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=out_features, kernel_size=3, padding=1, bias=False, padding_mode='zeros')

        self.dropout = nn.Dropout2d(0.2)
        self.pool = nn.AvgPool2d(4, 4)
        self.relu = nn.LeakyReLU()
        self.flatten = nn.Flatten()
        self.softmax = nn.Softmax()

    def forward(self, x):
        x = self.dropout(self.pool(self.relu(self.conv1(x))))
        x = self.dropout(self.pool(self.relu(self.conv2(x))))
        x = self.dropout(self.pool(self.relu(self.conv3(x))))
        x = self.flatten(x)
        x = self.softmax(x)
        return x