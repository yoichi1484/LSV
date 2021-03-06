from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
try:
  import japanize_matplotlib
except:
  pass

#from IPython.display import HTML
#from matplotlib import rc # for Jupyter
#rc('animation', html='jshtml') # for Jupyter

import numpy as np
#from collections import OrderedDict
from gensim.test.utils import common_texts
from gensim.models import word2vec
from gensim.models import KeyedVectors


class AnalogyVisualizer():
    def __init__(self, embedding):
        with open(embedding) as f:
            wv = f.read().split('\n')[1:-1]
        self.words = [w.split(' ')[0] for w in wv]
        vecs = np.array([self._to_array(w.split(' ')[1:]) for w in wv])
        self.xs, self.ys, self.zs = vecs.T[0], vecs.T[1], vecs.T[2]

    def _get_coordinates_of_annotation(self, analogy_pairs):
        coordinate = []
        analogy_words = analogy_pairs.flatten()
        for word, x,y,z in zip(self.words, self.xs, self.ys, self.zs):
            if word in analogy_words:
                coordinate.append((word, x,y,z))
        return coordinate

    def _get_coordinates_of_pairs(self, pairs):
        coordinate = []
        for pair in pairs:
            x = [v for v, w in zip(self.xs, self.words) if w in pair]
            y = [v for v, w in zip(self.ys, self.words) if w in pair]
            z = [v for v, w in zip(self.zs, self.words) if w in pair]
            assert x != []
            coordinate.append((x,y,z))
        return coordinate

    def _to_array(self, vecs):
        return np.array(vecs).astype(np.float32)

    def _update(self, i):
        self.ax.cla()
        self.plot()
        self.ax.view_init(elev=30., azim=3.6*i)
        return self.fig, 

    def plot(self):
        self.ax.plot(self.xs, self.ys, self.zs, marker="o", 
                     linestyle='None', color="green", alpha = 0.1) 
    
        # Plot analogy pairs
        for x, y, z in self.coordinate1:
            self.ax.plot(x, y, z, lw=2, color="red")
        
        for x, y, z in self.coordinate2:
            self.ax.plot(x, y, z, lw=2, color="blue")
        
        for word, x, y, z in self.coordinate3:
            self.ax.text(x, y, z, word)
            self.ax.plot([0., x], [0., y], [0., z], lw=1, color="k", linestyle="dashed")

        self.ax.text(0,0,0, "O") # Origin
        self.ax.plot([0], [0], [0], marker="o", linestyle='None', color="k", alpha = 1) 

    def animation(self, analogy_pairs):
        analogy_pairs = np.array(analogy_pairs)
        self.setup(analogy_pairs)
        self.fig = plt.figure(figsize = (8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        ani = animation.FuncAnimation(self.fig, self._update, #init_func=self.init,
                                       frames=100, interval=100, blit=True)
        return ani

    def setup(self, analogy_pairs):
        self.coordinate1 = self._get_coordinates_of_pairs(analogy_pairs)
        self.coordinate2 = self._get_coordinates_of_pairs(analogy_pairs.T)
        self.coordinate3 = self._get_coordinates_of_annotation(analogy_pairs)
