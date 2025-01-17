LSV: Latent Space Visualizer
====
A toolkit for visualizing latent space

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xPM_jG0PpLHjdv2YT08bzX8X80OXRHGS?usp=sharing) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE.txt)

# Usage
To visualize a latent space, the three-dimensional latent space should be trained in advance.
Alternatively, you can use the pre-trained embeddings in ```data/sgns_text8_3d.txt```.
```python
import gensim.downloader as api
from gensim.models import Word2Vec

dataset = api.load("text8")  
embedding = Word2Vec(dataset, size=3, min_count=1000, 
                     window=5, iter=100, sg=1, hs=0)
embedding.wv.save_word2vec_format("model.txt")   
```
Visualize word analogy
```python
import lsv
from gensim.models import KeyedVectors

embedding = KeyedVectors.load_word2vec_format("model.txt")
vi = lsv.visualizer.AnalogyVisualizer(embedding)
```
Plot word vectors
```python
vi.figure()
```
<div align="center">
<img src=https://github.com/yoichi1484/lsv/blob/main/docs/images/lsv_example1.jpg "visualize_example" width="50%" height="50%">
</div>

Make a 3D animation
```python
vi.animation()
```
<div align="center">
<img src=https://github.com/yoichi1484/lsv/blob/main/docs/images/lsv_example1.gif "visualize_example" width="50%" height="50%">
</div>

Visualization of analogy pairs
```python
analogy_pairs = [["king", "queen"], ["man", "woman"]]
vi.animation(analogy_pairs).save('latent_space1.mp4', writer="ffmpeg", dpi=100)
```
<div align="center">
<img src=https://github.com/yoichi1484/lsv/blob/main/docs/images/lsv_example2.gif "visualize_example" width="50%" height="50%">
</div>

Visualization of word frequency. The axis of the color bar is a log scale.
```python
word_freq = {"the":123456, "one":56789, ...}
vi = lsv.visualizer.AnalogyVisualizer(emb, word_freq = word_freq)
vi.animation().save('latent_space2.mp4', writer="ffmpeg", dpi=100)
```
<div align="center">
<img src=https://github.com/yoichi1484/lsv/blob/main/docs/images/lsv_example3.gif "visualize_example" width="50%" height="50%">
</div>
