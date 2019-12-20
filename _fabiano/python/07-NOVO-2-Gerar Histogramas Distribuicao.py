#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import util_ler_dados as udata

plt.style.use('seaborn-colorblind')


def gerarHistograma(rows, cols, ind, plt, df, desc, bins):
    ax = plt.subplot(rows, cols, ind)
    ax.set(ylabel='Quantity')#xlabel=desc,
    ax.axvline(float(df.median()), color='b')
    ax.axvline(float(df.mean()), color='r')
    sns.distplot(df, ax=ax, bins=bins, hist=True, kde=False)
    plt.title('%s' % (desc))  # , fontproperties=font_prop )


#     plt.title('%s: %s (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def gerarKdeHistograma(rows, cols, ind, plt, df, desc, bins):
    ax = plt.subplot(rows, cols, ind)
    ax.set(ylabel='f(mean)') #xlabel=desc,
    ax.axvline(float(df.median()), color='b')
    ax.axvline(float(df.mean()), color='r')
    sns.distplot(df, ax=ax, bins=bins, hist=True, kde=True) #fit=stats.gamma
    plt.title('%s (KDE)' % (desc))  # , fontproperties=font_prop )


#     plt.title('%s: %s (KDE) (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def gerarBoxplot(rows, cols, ind, plt, df, desc, palet='Set2'):
    ax = plt.subplot(rows, cols, ind)
    ax.axhline(float(df.median()), color='b')
    ax.axhline(float(df.mean()), color='r')
    sns.boxplot(data=df, ax=ax, palette=palet)
    # plt.title('%s' % (desc))  # , fontproperties=font_prop )
#     plt.title('%s: %s (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def definirSubGrafico(prob, size, algo, df, bins, font_size, salvar=True):
    data_unordered = df[[udata.obterNomeColuna('percentual_k_unordered')]]
    data_maior_array = df[[udata.obterNomeColuna('percentual_maior_array')]]
    rows = 2
    cols = 3
    ind = 1

    fig = plt.figure(figsize=[80, 60])
    plt.rcParams.update({'font.size': font_size})
    font_prop = font_manager.FontProperties(size=font_size, style='normal', weight='bold')
    plt.fontproperties = font_prop
    fig.suptitle('%s: (Prob.: %s, Size: %s)' % (algo, prob, size), fontsize=80)

    nbins = 30
    palet = sns.cubehelix_palette(8, start=.5, rot=-.75)  # 'Blues'

    # ===========================================================
    # data_maior_array
    # ===========================================================
    gerarHistograma(rows, cols, ind, plt, data_maior_array, udata.obterNomeColuna('percentual_maior_array'), bins)
    ind += 1

    gerarKdeHistograma(rows, cols, ind, plt, data_maior_array, udata.obterNomeColuna('percentual_maior_array'), bins)
    ind += 1

    gerarBoxplot(rows, cols, ind, plt, data_maior_array, udata.obterNomeColuna('percentual_maior_array'), palet=palet)
    ind += 1

    # ===========================================================
    # data_unordered
    # ===========================================================
    gerarHistograma(rows, cols, ind, plt, data_unordered, udata.obterNomeColuna('percentual_k_unordered'), bins)
    ind += 1

    gerarKdeHistograma(rows, cols, ind, plt, data_unordered, udata.obterNomeColuna('percentual_k_unordered'), bins)
    ind += 1

    gerarBoxplot(rows, cols, ind, plt, data_unordered, udata.obterNomeColuna('percentual_k_unordered'), palet=palet)
    ind += 1

    # ===========================================================
    # se for pra salvar o grafico
    # ===========================================================
    if (salvar):
        plt.savefig('../resultados/graficos-2/distribuicao/%s_%s_%s.png' % (prob, size, algo), bbox_inches='tight',
                    pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')

    print('Salvou Prob=%s, Tam=%s, ALg=%s'%(prob, size, algo))



# EXECUCAO ============================================================================

nbins = {100: 15, 1000: 30, 10000: 60}
sizes = [100, 1000, 10000]
probs = [0.01, 0.02, 0.05]

# sizes = [1000]
# probs = [0.01, 0.02, 0.05]

font_size = 60

i = 1

for prob in probs:
    for size in sizes:
        bins = nbins.get(size)

        df = udata.obterDados2()
        df = udata.filtrarPorProbabilidadeErro(df, prob=prob)
        df = udata.filtrarPorTamanhoArray(df, tamanho=size)

        df_bubble = df[df[udata.obterNomeColuna('algoritmo')] == 'bubble']
        df_merge = df[df[udata.obterNomeColuna('algoritmo')] == 'merge']
        df_insertion = df[df[udata.obterNomeColuna('algoritmo')] == 'insertion']
        df_quick = df[df[udata.obterNomeColuna('algoritmo')] == 'quick']

        # print(df_bubble.head())

        i = definirSubGrafico(prob, size, 'Bubble', df_bubble, bins, font_size)
        i = definirSubGrafico(prob, size, 'Merge', df_merge, bins, font_size)
        i = definirSubGrafico(prob, size, 'Quick', df_quick, bins, font_size)
        i = definirSubGrafico(prob, size, 'Insertion', df_insertion, bins, font_size)


