# QQ Plot
from numpy.random import seed
from numpy.random import randn
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt

import util_ler_dados as udata


# # seed the random number generator
# seed(1)
# # generate univariate observations
# data = 5 * randn(100) + 50
# # q-q plot

data = udata.obterDados(probs=[0.05], sizes=[100])

fig = plt.figure(figsize=[10, 5])
plt.suptitle('Titulo')
ax = plt.gca()

# qqplot(data=data[udata.COLUNA_MAIOR_ARRAY], line='s')
# qqplot(data=data[udata.COLUNA_DESORDENADOS], line='s')
# qqplot(data=data[udata.COLUNA_MAIOR_ARRAY_PERCENTUAL], line='s')
qqplot(ax=ax, data=data[udata.COLUNA_DESORDENADOS_PERCENTUAL], line='s')
plt.show()