import gensim
from src.utils import config
from src.data import pheme_dataloader_tweet_content
from sklearn.model_selection import train_test_split
from multiprocessing import cpu_count

def train_w2v():
    text_list, y = pheme_dataloader_tweet_content.load_data(config.DATA_PATH)

    model = direct_train_w2v(text_list)
    model.wv.save_word2vec_format('../../../pretrain_models/twitter_all_text_w2c_300_v1.txt', binary=False)

def direct_train_w2v(text_list):
    model = gensim.models.Word2Vec(text_list, size=300, window=10, min_count=5, iter=10, workers=cpu_count())
    return model

def update_model(model, data):
    model.build_vocab(data, update=True)
    model.train(data, total_examples=model.corpus_count, epochs=model.iter)
    return model

if __name__ == '__main__':
    train_w2v()