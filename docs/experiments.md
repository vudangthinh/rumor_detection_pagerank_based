### PTK

Time | Data | Pre-process | Accuracy
--- | --- | --- | ---
| | gurlitt-all-rnr-threads, ottawashooting-all-rnr-threads, putinmissing-all-rnr-threads (1266 tweets) | True | 0.5
| | | False | 0.58

### Baseline

Time | Data | Embed size | Pre-process | Accuracy
--- | --- | --- | --- | ---
| | PHEME_v2 | 200(w2v.twitter.27B.200d.txt) | Yes | Accuracy: 64.782
| | PHEME_v2 | 300(twitter_w2c_300_v1) | Yes | Accuracy: 65.664

### Pagerank

#### PHEME v1
Time | Data | Embed size | Pre-process | Model | Accuracy
--- | --- | --- | --- | --- | ---
| | PHEME_v1 | 300(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) - No pagerank, only source tweet | Acc: 0.679 P: 0.610 R: 0.364 F1: 0.370
| | PHEME_v1 | 300(CV-not update) | Yes | RF(n_estimators=200) | Acc: 0.706 P: 0.763 R: 0.358 F1: 0.473
| | PHEME_v1 | 300(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) | Acc: 0.776 P: 0.689 R: 0.612 F1: 0.636 (wrong: Acc: 0.753 P: 0.715 R: 0.599 F1: 0.638 (Acc: 0.753 P: 0.710 R: 0.612 F1: 0.642 / Acc: 0.758 P: 0.716 R: 0.597 F1: 0.645))
| | PHEME_v1 | 400(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) | Acc: 0.774 P: 0.685 R: 0.624 F1: 0.638
| | PHEME_v1 | 300(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) - Pagerank alpha: 0.8 | Acc: 0.779 P: 0.692 R: 0.613 F1: 0.639
| | PHEME_v1 + social features | 300(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) - Pagerank alpha: 0.8 | Acc: 0.780 P: 0.701 R: 0.614 F1: 0.642
| | PHEME_v1 + social features | 300(CV-update) | Yes | RF(n_estimators=300, max_depth=10, random_state=0) - Pagerank alpha: 0.8 | Acc: 0.783 P: 0.704 R: 0.616 F1: 0.647

| | PHEME_v1 | 200(CV-w2v.twitter.27B.200d.txt) | Yes | RF(n_estimators=200) | 


Degree centrality: Acc: 0.776 P: 0.688 R: 0.612 F1: 0.638 (normalized: Acc: 0.773 P: 0.690 R: 0.602 F1: 0.631)  
In Degree centrality: Acc: 0.766 P: 0.681 R: 0.602 F1: 0.617 (both normalized and not)  
Closeness: Acc: 0.772 P: 0.688 R: 0.609 F1: 0.630 (undirected graph: Acc: 0.765 P: 0.683 R: 0.547 F1: 0.602)  
Betweenness: Acc: 0.757 P: 0.692 R: 0.536 F1: 0.585 (undirected, unnormalized)  
Average: Acc: 0.761 P: 0.681 R: 0.513 F1: 0.579  
Harmonic: Acc: 0.775 P: 0.694 R: 0.613 F1: 0.633  
Second order centrality: Acc: 0.725 P: 0.634 R: 0.421 F1: 0.501 
 
Time reduce (log e): Acc: 0.779 P: 0.699 R: 0.607 F1: 0.640
Time reduce (log e): Acc: 0.781 P: 0.706 R: 0.601 F1: 0.641 (content and social features)
Time reduce (log 2): Acc: 0.781 P: 0.702 R: 0.611 F1: 0.641

Wayback PageRank (Weight back = 0.2): Acc: 0.779 P: 0.694 R: 0.619 F1: 0.643
Wayback PageRank: Acc: 0.782 P: 0.702 R: 0.614 F1: 0.644
Wayback PageRank: Acc: 0.779 P: 0.698 R: 0.607 F1: 0.639 (content and social features)



Centrality | Accuracy | Precision | Recall | F1
--- | --- | --- | --- | ---
Degree Centrality | 0.773 | 0.690 | 0.602 | 0.631
Closeness Centrality | 0.772 | 0.688 | 0.609 | 0.630
Betweenness Centrality | 0.757 | **0.692** | 0.536 | 0.585
Equal Centrality | 0.761 | 0.681 | 0.513 | 0.579
Second-order Centrality | 0.725 | 0.634 | 0.421 | 0.501
Pagerank Centrality | **0.779** | **0.692** | **0.613** | **0.639**

#### PHEME v2
Time | Data | Embed size | Pre-process | Model | Accuracy
--- | --- | --- | --- | --- | ---
| | PHEME_v2 | 100(w2v.twitter.27B.100d.txt) | Yes | RF | Acc: 0.733 P: 0.715 R: 0.490 F1: 0.581
| | PHEME_v2 | 200(w2v.twitter.27B.200d.txt) | Yes | RF | Acc: 0.752 P: 0.752 R: 0.514 F1: 0.611
| | PHEME_v2 | 300(twitter_w2c_300_v1) | Yes | RF | Acc: 0.771 P: 0.749 R: 0.594 F1: 0.663
| | PHEME_v2 (remove last url) | 300(twitter_w2c_300_v1) | Yes | RF | Acc: 0.762 P: 0.734 R: 0.580 F1: 0.648
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) | Yes | RF | Acc: 0.810 P: 0.799 R: 0.664 F1: 0.725
| | PHEME_v2 | 300(twitter_d2v.model) | Yes | RF | Acc: 0.692 P: 0.643 R: 0.417 F1: 0.506
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) + tfidf | Yes | RF | Acc: 0.812 P: 0.792 R: 0.680 F1: 0.732 (original data, if fix wrong data acc will reduce)
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) | Yes | RF(n_estimators=200, random_state=0) | Acc: 0.837 P: 0.818 R: 0.733 F1: 0.773
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) + tfidf | Yes | RF(n_estimators=200, random_state=0) | Acc: 0.841 P: 0.823 R: 0.738 F1: 0.778
| | PHEME_v2 | 200(w2v.twitter.27B.200d.txt) | Yes | RF(n_estimators=200, random_state=0) | Acc: 0.803 P: 0.823 R: 0.610 F1: 0.701


1. Try to run without pagerank for comparing


2. 
