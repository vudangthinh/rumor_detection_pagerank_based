* Try doc2vec
* Read Professor recommend paper
* Temporal Pagerank


### 1. Pre-process
1. lower + split by space
2. lower + ekphrasis + remove stopword

### 2. Word embedding
1. twitter_all_text_w2c_300_v1: data_v2, size=300, window=10, min_count=5, workers=20, iter=10

### 3. Sentence embedding
1. average of word vector
2. average of word vector with tf-idf
3. doc2vec

Method 2 is not better than method 1

### 4. Graph embedding
1. Static Pagerank
2. Temporal Pagerank

We need Pagerank, Pagerank gives better results than averaged vector of all nodes.

### 5. Training method