LSV: Latent Space Visualizer
====
A toolkit for visualizing latent space

Demo page: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xPM_jG0PpLHjdv2YT08bzX8X80OXRHGS?usp=sharing)

# Usage
```python
import lsv

# for Jupyter
from IPython.display import HTML
from matplotlib import rc 
rc('animation', html='jshtml') 
%config InlineBackend.figure_formats = {'png', 'retina'}
%matplotlib inline

vi = lsv.visualizer.AnalogyVisualizer("/content/sake_embedding/src/model.txt")

analogy_pairs = [["king", "queen"], ["man", "woman"]], 
ani = vi.animation(analogy_pairs)
ani
```

```
<div align="center">
<img src=https://github.com/ahclab/quantum/blob/master/docs/image/sampled_vectors_basic_1.gif "visualize_example3">
</div>
```
