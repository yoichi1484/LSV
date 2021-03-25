from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
try:
    import japanize_matplotlib
except:
    pass

import numpy as np
import random
#from collections import OrderedDict
from gensim.test.utils import common_texts
from gensim.models import word2vec
from gensim.models import KeyedVectors


class AnalogyVisualizer():
    def __init__(self, embedding, max_num_vecs = 20000, word_freq = None):
        self.embedding = embedding
        words = embedding.wv.index2word
        if not word_freq is None:
            words = [word for word in words if word in word_freq]
        
        # Sampling word vectors
        max_num_vecs = len(words) if len(words) < max_num_vecs else max_num_vecs
        indexes = random.sample(list(range(len(words))), max_num_vecs)
        
        if word_freq is None:
            self.words = [w for i, w in enumerate(words) if i in indexes]
            self.word_freq = word_freq
        else:
            self.words = [w for i, w in enumerate(words) if i in indexes]
            self.word_freq = np.array([np.log10(word_freq[word]) for word in self.words])
        
        # vectors
        vecs = self.embedding[self.words]
        
        # x,y,z
        self.xs, self.ys, self.zs = vecs.T[0], vecs.T[1], vecs.T[2]
        self.plot_analogy_pairs = False

    def _get_coordinates_of_annotation(self, analogy_pairs):
        coordinate = []
        analogy_words = analogy_pairs.flatten()
        for word in analogy_words:
            v = self.embedding[word]
            assert len(v) == 3, "vector dimension should be three, but {}".format(len(v))
            x, y, z = v.T[0], v.T[1], v.T[2]
            coordinate.append((word, x,y,z))
        return coordinate

    def _get_coordinates_of_pairs(self, pairs):
        coordinate = []
        for pair in pairs:
            for word in pair:
                v = self.embedding[word]
                assert len(v) == 3, "vector dimension should be three, but {}".format(len(v))
                x, y, z = v.T[0], v.T[1], v.T[2]
                coordinate.append((x,y,z))
        return coordinate

    def _to_array(self, vecs):
        return np.array(vecs).astype(np.float32)

    def _update(self, i):
        self.ax.cla()
        self.plot()
        self.ax.view_init(elev=30., azim=3.6*i)
        if not self.word_freq is None and self.pltcolorbar:
            cbar = self.fig.colorbar(self.sc, shrink=0.5, aspect=20, ax=self.ax, 
                                     norm=LogNorm(vmin=self.word_freq.min(), vmax=self.word_freq.max())) 
            cbar.set_clim(self.word_freq.min(), self.word_freq.max())
            self.pltcolorbar = False
        return self.fig, 

    def plot(self):
        # Plot vectors
        if self.word_freq is None:
            self.ax.plot(self.xs, self.ys, self.zs, 
                         linestyle='None', color="green", marker='.', alpha = 0.1)
            #self.ax.scatter3D(self.xs, self.ys, self.zs, 
            #                  color="green", alpha = 0.1)
        else:
            self.sc = self.ax.scatter3D(self.xs, self.ys, self.zs, 
                              c=self.word_freq, cmap='jet', s=0.5, marker='.')#, alpha = 0.1)
    
        # Plot analogy pairs
        if self.plot_analogy_pairs:
            self.coordinate1 = np.array(self.coordinate1)
            xs, ys, zs = self.coordinate1.T[0], self.coordinate1.T[1], self.coordinate1.T[2]
            self.ax.plot(xs[:2], ys[:2], zs[:2], lw=2, color="red", alpha = 0.6)
            self.ax.plot(xs[2:], ys[2:], zs[2:], lw=2, color="red", alpha = 0.6)
            self.ax.plot(xs[::2], ys[::2], zs[::2], lw=2, color="blue", alpha = 0.6)
            self.ax.plot(xs[1::2], ys[1::2], zs[1::2], lw=2, color="blue", alpha = 0.6)
        
            #self.coordinate2 = np.array(self.coordinate2)
            #xs, ys, zs = self.coordinate2.T[0], self.coordinate2.T[1], self.coordinate2.T[2]
            #self.ax.plot(xs, ys, zs, lw=2, color="blue")
        
            # Plot words
            for word, x, y, z in self.coordinate3:
                self.ax.text(x, y, z, word)
                self.ax.plot([0., x], [0., y], [0., z], lw=1, color="k", linestyle="dashed", alpha = 0.1)

        # Plot origin
        self.ax.text(0,0,0, "O") # Origin
        self.ax.plot([0], [0], [0], marker="o", linestyle='None', color="k", alpha = 0.6)
        
    def setup(self, analogy_pairs):
        self.coordinate1 = self._get_coordinates_of_pairs(analogy_pairs)
        #self.coordinate2 = self._get_coordinates_of_pairs(analogy_pairs.T)
        self.coordinate3 = self._get_coordinates_of_annotation(analogy_pairs)

    def animation(self, analogy_pairs=None):
        if analogy_pairs is None:
            self.plot_analogy_pairs = False
        else:
            self.plot_analogy_pairs = True
            analogy_pairs = np.array(analogy_pairs)
            self.setup(analogy_pairs)
        self.fig = plt.figure(figsize = (8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        if not self.word_freq is None:
            self.pltcolorbar = True
        ani = animation.FuncAnimation(self.fig, self._update, #init_func=self.init,
                                       frames=100, interval=100, blit=True)
        return ani

    def figure(self, analogy_pairs=None):
        if analogy_pairs is None:
            self.plot_analogy_pairs = False
        else:
            self.plot_analogy_pairs = True
            analogy_pairs = np.array(analogy_pairs)
            self.setup(analogy_pairs)
        self.fig = plt.figure(figsize = (8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        if not self.word_freq is None:
            self.pltcolorbar = True
        self.plot()
        if not self.word_freq is None and self.pltcolorbar:
            cbar = self.fig.colorbar(self.sc, shrink=0.5, aspect=20, ax=self.ax, 
                                     norm=LogNorm(vmin=self.word_freq.min(), vmax=self.word_freq.max())) 
            cbar.set_clim(self.word_freq.min(), self.word_freq.max())
            self.pltcolorbar = False
        return self.fig, self.ax
