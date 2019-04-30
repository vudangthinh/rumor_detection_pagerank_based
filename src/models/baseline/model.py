import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Module

torch.manual_seed(1)

def create_emb_layer(word_vectors, trainable=False):
    weights = torch.FloatTensor(word_vectors.vectors)
    oov_vector = torch.zeros([1, weights.shape[1]])
    weights = torch.cat((weights, oov_vector), 0)

    embedding = nn.Embedding.from_pretrained(weights)
    embedding.weight.requires_grad = trainable

    return embedding

class Net(Module):
    def __init__(self, word_vectors, hidden_dim, target_size):
        super(Net, self).__init__()
        input_dim = word_vectors.vector_size

        self.embedding = create_emb_layer(word_vectors, False)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=1)
        self.linear = nn.Linear(hidden_dim, target_size)

    def forward(self, input_):
        embed_vector = self.embedding(input_)
        embed_vector.transpose_(1, 0)
        lstm_output, lstm_hidden = self.lstm(embed_vector)
        output = self.linear(lstm_hidden[0])

        return output