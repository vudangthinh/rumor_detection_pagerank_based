import gensim
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from src.utils import config
from src.data import pheme_dataloader_tweet_content

def create_tagged_document(text_list):
    for i, tokens in enumerate(text_list):
        yield TaggedDocument(tokens, [i])

def process():
    text_list, y = pheme_dataloader_tweet_content.load_data(config.DATA_PATH)
    train_data = list(create_tagged_document(text_list))
    model = Doc2Vec(vector_size=300, min_count=5, epochs=10)
    model.build_vocab(train_data)
    model.train(train_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('../../../pretrain_models/twitter_d2v.model')

if __name__ == '__main__':
    process()