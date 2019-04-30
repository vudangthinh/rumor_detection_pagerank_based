import torch
from src.models.baseline import pheme_dataset
from torch.utils.data import DataLoader, random_split
from src.utils import config
from src.models.baseline import model
from gensim.models import KeyedVectors
from src.utils import config

word_vectors = KeyedVectors.load_word2vec_format(config.EMBEDDING_FILE, binary=False)

dataset = pheme_dataset.PHEME_Dataset(config.DATA_PATH, word_vectors)
dataset_size = len(dataset)
train_size = int(0.7 * dataset_size)
valid_size = dataset_size - train_size
print("Dataset size:", dataset_size)

train_dataset, valid_dataset = random_split(dataset, (train_size, valid_size))
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True, num_workers=8)
valid_loader = DataLoader(valid_dataset, batch_size=1, shuffle=False, num_workers=8)

n_epoches = 5
hidden_dim = 200
target_size = 2
train_model = model.Net(word_vectors, hidden_dim, target_size)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(train_model.parameters(), lr=1e-4)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print('Device:', device)

train_model.to(device)
train_model.train()

for epoch in range(n_epoches):
    running_loss = 0

    for i_batch, (text_embed, label) in enumerate(train_loader):
        text_embed = text_embed.to(device)
        label = label.to(device)
        if label == 0:
            label = torch.LongTensor([0, 1])
        else:
            label = torch.LongTensor([1, 0])

        print(text_embed.shape)

        pred = train_model(text_embed)
        print(pred.shape)
        loss = criterion(pred, label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i_batch % 100 == 99:
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i_batch + 1, running_loss / 100))
            running_loss = 0.0