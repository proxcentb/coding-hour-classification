import torch
import torch.nn.functional as F
import torch.optim as optim
from model import Net
from torchsummary import summary
from tqdm import tqdm
from torchvision.transforms import Compose, Compose, ToTensor, RandomAffine, Grayscale
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, ConcatDataset

device = 'cuda'

transforms = Compose([
    Grayscale(),
    RandomAffine(degrees=(-10, 10), translate=(0.2, 0.2), scale=(0.5, 1.1)),
    ToTensor()
])

train_dataset = ConcatDataset([ImageFolder(root='sorted_images/train', transform=transforms) for i in range(0, 100)])
test_dataset = ConcatDataset([ImageFolder(root='sorted_images/test', transform=transforms) for i in range(0, 100)])

train_loader = DataLoader(train_dataset, batch_size=1)
test_loader = DataLoader(test_dataset, batch_size=1)

labels = train_dataset.datasets[0].class_to_idx

model = Net(len(labels)).to(device)
summary(model, input_size=(1, 64, 64))

optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.75)

def train(model, epoch):
    model.train()
    progress_bar = tqdm(train_loader)
    for batch_index, (data, target) in enumerate(progress_bar):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
        progress_bar.set_description(desc=f'epoch: {epoch} loss={loss.item()} batch_index={batch_index}')

def test(model):
    model.eval()
    test_loss = 0
    correct_guesses = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.cross_entropy(output, target, reduction='sum').item()
            predictions = output.argmax(dim=1, keepdim=True)
            correct_guesses += predictions.eq(target.view_as(predictions)).sum().item()
    test_loss /= len(test_loader.dataset)

    print('Test set: Average loss: {:.4f}, Accuracy Test: {}/{} ({:.1f}%)'.format(
        test_loss, 
        correct_guesses,
        len(test_loader.dataset), 100. * correct_guesses / len(test_loader.dataset)
    ))

for epoch in range(0, 6):
    train(model, epoch)
    test(model)

torch.save(model, "model.pth")