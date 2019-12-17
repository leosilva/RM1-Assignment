#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
import util_ler_dados as udata

plt.style.use('seaborn-colorblind')


def gerarHistograma(rows, cols, ind, plt, df, desc, prob, size, algo):
    ax = plt.subplot(rows, cols, ind)
    ax.set(xlabel=desc, ylabel='quantidade')
    ax.axvline(float(df.median()), color='b')
    ax.axvline(float(df.mean()), color='r')
    sns.distplot(df, ax=ax, bins=nbins, hist=True, kde=False)
    plt.title('%s' % (desc))  # , fontproperties=font_prop )


#     plt.title('%s: %s (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def gerarKdeHistograma(rows, cols, ind, plt, df, desc, prob, size, algo):
    ax = plt.subplot(rows, cols, ind)
    ax.set(xlabel=desc, ylabel='quantidade')
    ax.axvline(float(df.median()), color='b')
    ax.axvline(float(df.mean()), color='r')
    sns.distplot(df, ax=ax, bins=nbins, hist=True, kde=True)
    plt.title('%s (KDE)' % (desc))  # , fontproperties=font_prop )


#     plt.title('%s: %s (KDE) (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def gerarBoxplot(rows, cols, ind, plt, df, desc, prob, size, algo, palet='Set2'):
    ax = plt.subplot(rows, cols, ind)
    ax.axhline(float(df.median()), color='b')
    ax.axhline(float(df.mean()), color='r')
    sns.boxplot(data=df, ax=ax, palette=palet)
    plt.title('%s' % (desc))  # , fontproperties=font_prop )
#     plt.title('%s: %s (Prob: %s, Tam: %s)' % (algo, desc, prob, size))#, fontproperties=font_prop )


def definirSubGrafico(prob, size, algo, df, nbins, font_size, salvar=True):
    data_unordered = df[['percentual_k_unordered']]
    data_maior_array = df[['percentual_maior_array']]
    rows = 2
    cols = 3
    ind = 1

    fig = plt.figure(figsize=[80, 60])
    plt.rcParams.update({'font.size': font_size})
    font_prop = font_manager.FontProperties(size=font_size, style='normal', weight='bold')
    plt.fontproperties = font_prop
    fig.suptitle('%s: (Prob: %s, Tam: %s)' % (algo, prob, size), fontsize=80)

    nbins = 30
    palet = sns.cubehelix_palette(8, start=.5, rot=-.75)  # 'Blues'

    # ===========================================================
    # data_maior_array
    # ===========================================================
    gerarHistograma(rows, cols, ind, plt, data_maior_array, '% Maior Array', prob, size, algo)
    ind += 1

    gerarBoxplot(rows, cols, ind, plt, data_maior_array, '% Maior Array', prob, size, algo, palet=palet)
    ind += 1

    gerarKdeHistograma(rows, cols, ind, plt, data_maior_array, '% Maior Array', prob, size, algo)
    ind += 1

    # ===========================================================
    # data_unordered
    # ===========================================================
    gerarHistograma(rows, cols, ind, plt, data_unordered, '% Desordenados', prob, size, algo)
    ind += 1

    gerarBoxplot(rows, cols, ind, plt, data_unordered, '% Desordenados', prob, size, algo, palet=palet)
    ind += 1

    gerarKdeHistograma(rows, cols, ind, plt, data_unordered, '% Desordenados', prob, size, algo)
    ind += 1

    # ===========================================================
    # se for pra salvar o grafico
    # ===========================================================
    if (salvar):
        plt.savefig('graficos-2/distribuicao/%s_%s_%s.png' % (prob, size, algo), bbox_inches='tight',
                    pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')



# EXECUCAO ============================================================================

sizes = [100, 1000, 10000]
probs = [0.01, 0.02, 0.05]

nbins = 20
font_size = 50

i = 1

for prob in probs:
    for size in sizes:

        df = udata.obterDados2()
        df = udata.filtrarPorProbabilidadeErro(df, prob=prob)
        df = udata.filtrarPorTamanhoArray(df, tamanho=size)

        df_bubble = df[df['algoritmo'] == 'bubble']
        df_merge = df[df['algoritmo'] == 'merge']
        df_insertion = df[df['algoritmo'] == 'insertion']
        df_quick = df[df['algoritmo'] == 'quick']

        print(df_bubble.head())

        i = definirSubGrafico(prob, size, 'Bubble', df_bubble, nbins, font_size)
        i = definirSubGrafico(prob, size, 'Merge', df_merge, nbins, font_size)
        i = definirSubGrafico(prob, size, 'Quick', df_quick, nbins, font_size)
        i = definirSubGrafico(prob, size, 'Insertion', df_insertion, nbins, font_size)


