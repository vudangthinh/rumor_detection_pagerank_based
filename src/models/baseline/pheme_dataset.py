import torch
from torch.utils.data import Dataset, DataLoader
from src.data import pheme_dataloader_baseline


class PHEME_Dataset(Dataset):
    def __init__(self, data_path, word_vectors):
        super(PHEME_Dataset, self).__init__()
        self.text_list, self.y = pheme_dataloader_baseline.load_data(data_path)
        self.data = []
        for tokens in self.text_list:
            token_index_list = []
            for token in tokens:
                if token in word_vectors:
                    token_index = word_vectors.vocab[token].index
                else:
                    # print(token)
                    token_index = len(word_vectors.wv.vocab)

                token_index_list.append(token_index)

            token_tensor = torch.LongTensor(token_index_list)
            self.data.append(token_tensor)

    def __getitem__(self, item):
        return (self.data[item], self.y[item])

    def __len__(self):
        return len(self.data)