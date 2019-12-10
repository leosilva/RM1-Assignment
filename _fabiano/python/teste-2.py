#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_graficos as graf
from scipy.stats.distributions import norm

from scipy.stats import kde

x1 = np.random.normal(-1, 0.5, 15)

# parameters: (loc=0.0, scale=1.0, size=None)

x2 = np.random.normal(6, 1, 10)
y = np.r_[x1, x2]

# r_ Translates slice objects to concatenation along the first axis.

x = np.linspace(min(y), max(y), 100)
s = 0.4   # Smoothing parameter

kernels = np.transpose([norm.pdf(x, yi, s) for yi in y])

# Calculate the kernels
density = kde.gaussian_kde(y)

# plt.plot(x, kernels, 'k:')
# plt.plot(x, kernels.sum(1), 'r')
# plt.plot(y, np.zeros(len(y)), 'bo', ms=10)

xgrid = np.linspace(x.min(), x.max(), 200)
# plt.hist(y, bins=28, normed=True)
# plt.plot(xgrid, density(xgrid), 'r-')

# Create a bi-modal distribution with a mixture of Normals.

x1 = np.random.normal(-1, 2, 15) # parameters: (loc=0.0, scale=1.0, size=None)
x2 = np.random.normal(6, 3, 10)

# Append by row
x = np.r_[x1, x2]

# r_ Translates slice objects to concatenation along the first axis.
# plt.hist(x, bins=18, normed=True)


density = kde.gaussian_kde(x)
xgrid = np.linspace(x.min(), x.max(), 200)
plt.hist(x, bins=18, normed=True)
plt.plot(xgrid, density(xgrid), 'r-')

plt.show()