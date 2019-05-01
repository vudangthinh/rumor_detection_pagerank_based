import gensim
from src.utils import config
from src.data import pheme_dataloader_baseline

def process():
    text_list, y = pheme_dataloader_baseline.load_data(config.DATA_PATH)
    model = gensim.models.Word2Vec(text_list, size=300, window=10, min_count=5, workers=20, iter=10)
    model.wv.save_word2vec_format('../../../pretrain_models/twitter_w2c_300_v1.txt', binary=False)

if __name__ == '__main__':
    process()