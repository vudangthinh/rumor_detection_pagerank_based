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
| | PHEME_v2 | 100(w2v.twitter.27B.100d.txt) | Yes | Accuracy: 0.733402489626556 <br>Precision: 0.7154308617234469 <br>Recall: 0.4897119341563786 <br>F1: 0.5814332247557004
| | PHEME_v2 | 200(w2v.twitter.27B.200d.txt) | Yes | Accuracy: 0.7520746887966805 <br>Precision: 0.751503006012024 <br>Recall: 0.51440329218107 <br>F1: 0.6107491856677525
| | PHEME_v2 | 300(twitter_w2c_300_v1) | Yes | Accuracy: 0.7712655601659751 <br>Precision: 0.7491349480968859 <br>Recall: 0.5939643347050755 <br>F1: 0.6625860749808722
| | PHEME_v2 (remove last url) | 300(twitter_w2c_300_v1) | Yes | Accuracy: 0.7619294605809128 <br>Precision: 0.734375 <br>Recall: 0.5802469135802469 <br>F1: 0.6482758620689656
| | PHEME_v2 | 300(twitter_all_text_w2c_300_v1) | Yes | Accuracy: 0.8096473029045643 <br>Precision: 0.7986798679867987 <br>Recall: 0.663923182441701 <br>F1: 0.7250936329588015

1. Try to run without pagerank for comparing


2. 