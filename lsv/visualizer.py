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
import random
#from collections import OrderedDict
from gensim.test.utils import common_texts
from gensim.models import word2vec
from gensim.models import KeyedVectors


class AnalogyVisualizer():
    def __init__(self, embedding, max_num_vecs = 20000):
        self.embedding = embedding
        words = embedding.wv.index2word
        max_num_vecs = len(words) if len(words) < max_num_vecs
        indexes = random.sample(list(range(len(words))), max_num_vecs)
        self.words = [w for i, w in enumerate(words) if i in indexes]
        vecs = self.embedding[self.words]
        self.xs, self.ys, self.zs = vecs.T[0], vecs.T[1], vecs.T[2]

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
                #print(x,y,z)
                #assert False
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
        self.coordinate1 = np.array(self.coordinate1)
        xs, ys, zs = self.coordinate1.T[0], self.coordinate1.T[1], self.coordinate1.T[2]
        self.ax.plot(xs, ys, zs, lw=2, color="red")
        
        self.coordinate2 = np.array(self.coordinate2)
        xs, ys, zs = self.coordinate2.T[0], self.coordinate2.T[1], self.coordinate2.T[2]
        self.ax.plot(xs, ys, zs, lw=2, color="blue")
        
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
