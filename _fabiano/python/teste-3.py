#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_graficos as graf
import util_ler_dados as udata
from scipy.stats.distributions import norm

from scipy.stats import kde

df = udata.obterDados()

# for prob in udata.PROBABILIDADES:
df_prob = udata.filtrarPorProbabilidadeErro(df, '0.01')
print( df_prob.shape)
print( df_prob['algoritmo'].unique())

# print( df_prob.groupby(['size_of_array', 'algoritmo']).count().head() )

sns.lmplot(x='percentual_k_unordered',
           hue='algoritmo',
           y='percentual_maior_array',
           data=df,
           # markers=['o','v','+','x'],
           scatter_kws={'s': 5},
           col='algoritmo',
           row='probabilidade_erro', # 'size_of_array',
           height=3,
           )

# plt.show()
file_title = 'teste-03-lmplot'
plt.savefig('graficos/_%s.png' % (file_title), bbox_inches='tight',
            pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')

# print( df.head() )
#
# df1 = udata.filtrarPorProbabilidadeErro(df, '0.02')
# print( df1.head() )
#
# df2 = udata.filtrarPorAlgoritmo(df1, 'merge')
# print( df2.head() )
#
# df_means, df_std, df_min, df_max, df_var = udata.obterEstatisticasPorTamanho_Algoritmo(df1)
# print( df_means.head() )

