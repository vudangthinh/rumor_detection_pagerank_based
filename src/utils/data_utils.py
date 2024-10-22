from src.data import pheme_dataloader_baseline
from src.utils import config
from sklearn.model_selection import train_test_split
import json
import numpy as np


def split_dataset():
    train_test_dict = {}
    all_tweet_ids = pheme_dataloader_baseline.load_all_tweet_ids(config.DATA_PATH)

    tweet_train, tweet_test = train_test_split(all_tweet_ids)
    train_test_dict['train'] = tweet_train
    train_test_dict['test'] = tweet_test

    with open(config.SPLIT_DATA_FILE, 'w') as writer:
        json.dump(train_test_dict, writer)

def shuffle_data(train_list, label_list):
    indices = np.arange(train_list.shape[0])
    np.random.shuffle(indices)

    train_list = train_list[indices]
    label_list = label_list[indices]
    return train_list, label_list

if __name__ == '__main__':
    split_dataset()