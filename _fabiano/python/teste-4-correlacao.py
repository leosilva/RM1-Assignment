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

def salvarGrafico(df_p, file_title, tam):
    # df_p.loc[:]['size_of_array'] = tam
    print(df_p['size_of_array'].unique())
    corr = df_p.corr()#.round(decimal=3)
    print(corr)
    fig = plt.figure()
    sns.heatmap(corr, annot=True)#, cmap='coolwarm')
    fig.savefig('graficos/_%s.png' % (file_title), bbox_inches='tight',
                pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
    plt.close(fig)

q1 = udata.obterDados()
q1 = udata.filtrarPorTamanhoArray(q1, 100)
print(q1.corr())

df = udata.obterDados()
# salvarGrafico(df=df, file_title='teste-04-correlacao-0-geral')

for prob in udata.PROBABILIDADES:
    df_prob = udata.filtrarPorProbabilidadeErro(df, prob)
    # print( df_prob.shape )
    # print(df_alg.shape)
    for tam in udata.TAMANHOS:
        # print('%.2f-%s-%s' % (prob, alg, tam))
        df_tam = udata.filtrarPorTamanhoArray(df_prob, tam)
        for alg in udata.ALGORTIMOS:
            df_alg = udata.filtrarPorAlgoritmo(df_tam, alg)
            # print(df_tam.head())
            # print(df_tam.shape)
            # print('')
            # se tiver dados no DF
            if (df_alg.shape[0] > 0):
                print(df_alg.head())
                df_alg.loc[:]['size_of_array'] = tam * 1.0
                file_title = 'teste-04-correlacao-%s-%s-%s' % (prob, alg, tam)
                salvarGrafico(df_p=df_alg, file_title=file_title, tam=int(tam))
                break
            break
        break
    break