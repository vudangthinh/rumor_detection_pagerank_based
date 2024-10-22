import torch
from src.models.baseline import pheme_dataset
from torch.utils.data import DataLoader, random_split
from src.utils import config
from src.models.baseline import model_baseline
from gensim.models import KeyedVectors
from src.utils import config


n_epoches = 10
hidden_dim = 200
target_size = 2
batch_size = 1

word_vectors = KeyedVectors.load_word2vec_format(config.EMBEDDING_FILE, binary=False)

dataset = pheme_dataset.PHEME_Dataset(config.DATA_PATH, word_vectors)
dataset_size = len(dataset)
train_size = int(0.7 * dataset_size)
valid_size = dataset_size - train_size
print("Dataset size:", dataset_size)

train_dataset, valid_dataset = random_split(dataset, (train_size, valid_size))
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=8)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=8)

train_model = model_baseline.Net(word_vectors, hidden_dim, target_size)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(train_model.parameters(), lr=1e-4)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print('Device:', device)

train_model.to(device)
train_model.train()

for epoch in range(n_epoches):
    running_loss = 0
    correct = 0

    for i_batch, (text_embed, label) in enumerate(train_loader):
        text_embed = text_embed.to(device)
        label = label.to(device)
        # print(text_embed.shape)

        pred = train_model(text_embed)
        loss = criterion(pred, label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(pred.data, 1)
        correct += (predicted == label).sum().item()
        if i_batch % 1000 == 999:
            print('[%d, %5d] loss: %.3f acc: %.3f' %
                  (epoch + 1, i_batch + 1, running_loss / 1000, correct * 100.0 / (1000 * batch_size)))
            running_loss = 0.0
            correct = 0

# Test
train_model.eval()
total = 0
correct = 0

with torch.no_grad():
    for text_embed, label in valid_loader:
        text_embed = text_embed.to(device)
        label = label.to(device)

        pred = train_model(text_embed)
        total += label.size(0)
        _, predicted = torch.max(pred.data, 1)
        correct += (predicted == label).sum().item()

print('Valid Accuracy: %.3f' % (correct * 100.0 / total))

