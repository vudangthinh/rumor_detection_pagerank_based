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

Time | Data | Embed size | Pre-process | Accuracy
--- | --- | --- | --- | ---
| | PHEME_v2 | 100(w2v.twitter.27B.100d.txt) | Yes | Acc: 0.733 P: 0.715 R: 0.490 F1: 0.581
| | PHEME_v2 | 200(w2v.twitter.27B.200d.txt) | Yes | Acc: 0.752 P: 0.752 R: 0.514 F1: 0.611
| | PHEME_v2 | 300(twitter_w2c_300_v1) | Yes | Acc: 0.771 P: 0.749 R: 0.594 F1: 0.663
| | PHEME_v2 (remove last url) | 300(twitter_w2c_300_v1) | Yes | Acc: 0.762 P: 0.734 R: 0.580 F1: 0.648
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) | Yes | Acc: 0.810 P: 0.799 R: 0.664 F1: 0.725
| | PHEME_v2 | 300(twitter_d2v.model) | Yes | Acc: 0.692 P: 0.643 R: 0.417 F1: 0.506



1. Try to run without pagerank for comparing


2. 