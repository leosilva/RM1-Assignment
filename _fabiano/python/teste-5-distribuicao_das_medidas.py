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

def salvarGrafico(df, file_title, tam, prob, alg, bins=30):

    # numeros = df['percentual_maior_array']

    fig = plt.figure(figsize=[20, 15])
    plt.suptitle('%s - Prob. Erro: %s - Tam. Array: %s'%(alg, str(prob), str(tam)) )

    numeros = df['percentual_k_unordered']
    ax = plt.subplot(2,2,1)
    # ax.set_xlabel('% Desornados', labelpad=10, weight='bold', size=9)
    plt.title('% Desordenados')
    sns.distplot(numeros, ax=ax, bins=bins, hist=True, kde=False)

    ax = plt.subplot(2,2,2)
    # ax.set_xlabel('% Desornados', labelpad=10, weight='bold', size=9)
    plt.title('% Desordenados (KDE)')
    sns.distplot(numeros, ax=ax, bins=bins, hist=True, kde=True)

    numeros = df['percentual_maior_array']
    ax = plt.subplot(2,2,3)
    # ax.set_xlabel('% Maior Array', labelpad=10, weight='bold', size=9)
    plt.title('% Maior Array')
    sns.distplot(numeros, ax=ax, bins=bins, hist=True, kde=False)

    ax = plt.subplot(2,2,4)
    # ax.set_xlabel('% Maior Array', labelpad=10, weight='bold', size=9)
    plt.title('% Maior Array (KDE)')
    sns.distplot(numeros, ax=ax, bins=bins, hist=True, kde=True)

    fig.savefig('graficos/distribuicao_medidas/_%s.png' % (file_title), bbox_inches='tight',
                pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
    plt.close(fig)
    # plt.show()

    # fig = plt.figure(figsize=[40, 50])
    # plt.title('Prob. Erro: %s - Tam. Array: %s'%(str(prob), str(tam)) )
    # plt.subplot(6,2,1)
    # plt.hist(numeros, bins=bins)
    # plt.subplot(6,2,2)
    # plt.hist(numeros, bins=bins)
    # fig.savefig('graficos/distribuicao_medidas/_%s.png' % (file_title), bbox_inches='tight',
    #             pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
    # plt.close(fig)

    # # df_p.loc[:]['size_of_array'] = tam
    # print(df_p['size_of_array'].unique())
    # corr = df_p.corr()#.round(decimal=3)
    # print(corr)
    # fig = plt.figure()
    # sns.heatmap(corr, annot=True)#, cmap='coolwarm')
    # fig.savefig('graficos/distribuicao_medidas/_%s.png' % (file_title), bbox_inches='tight',
    #             pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
    # plt.close(fig)

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
                file_title = 'distribuicao_medidas_%s_%s_%s' % (prob, alg, tam)
                salvarGrafico(df=df_alg, file_title=file_title, tam=int(tam), prob=prob, alg=alg)
                break
            break
        break
    break