#imports
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import util_ler_dados as udata

plt.style.use('seaborn-colorblind')

def salvarPairplot(data, algoritmo, prob, size):
    fig = plt.figure()  # figsize=[80, 60])
    # plt.rcParams.update({'font.size': font_size})
    # plt.fontproperties = font_prop
    # fig.suptitle('%s: (Prob.: %s, Size: %s)' % (algo, prob, size), fontsize=80)
    sns.pairplot(data=data)
    plt.savefig('../resultados/04-linear_regression/%s_prob_%s_size_%s.png' % (algoritmo, prob, size),
                bbox_inches='tight'
                , pad_inches=2)
    plt.close()

def salvar(df, prob, size):
    salvarPairplot(df, 'tudo', prob, size)

    df_bubble = df[df['Sorting_algorithm'] == 'bubble']
    salvarPairplot(df_bubble, 'bubble', prob, size)

    df_merge = df[df['Sorting_algorithm'] == 'merge']
    salvarPairplot(df_merge, 'merge', prob, size)

    df_insertion = df[df['Sorting_algorithm'] == 'insertion']
    salvarPairplot(df_insertion, 'insertion', prob, size)

    df_quick = df[df['Sorting_algorithm'] == 'quick']
    salvarPairplot(df_quick, 'quick', prob, size)


# EXECUCAO ============================================================================

nbins = {100: 15, 1000: 30, 10000: 60}
sizes = [100, 1000, 10000]
probs = [0.01, 0.02, 0.05]

sizes = [1000]
probs = [0.01, 0.02, 0.05]

font_size = 60
font_prop = font_manager.FontProperties(size=font_size, style='normal', weight='bold')

i = 1

df_original = udata.obterDados2()
df_original = df_original[
    ['Probability_of_failure', 'Array_size', 'Sorting_algorithm', 'Perc_unordered_elements_quantity']]

# inserer coluna 'Sorting_algorithm_code', com valores numericos para os algoritmos
condicao = [df_original['Sorting_algorithm'] == 'bubble',
            df_original['Sorting_algorithm'] == 'merge',
            df_original['Sorting_algorithm'] == 'insertion',
            df_original['Sorting_algorithm'] == 'quick',
            ]
resultados = [1, 2, 3, 4]
df_original['Sorting_algorithm_code'] = np.select(condicao, resultados, -1)

#inicia salvamento dos graficos
salvar(df_original, 'ALL', 'ALL')

for prob in probs:
    df = udata.filtrarPorProbabilidadeErro(df_original, prob=prob)
    salvar(df=df, prob=prob, size='ALL')

for size in sizes:
    df = udata.filtrarPorTamanhoArray(df_original, tamanho=size)
    salvar(df=df, prob='ALL', size=size)

for prob in probs:
    for size in sizes:
        df = df_original
        df = udata.filtrarPorProbabilidadeErro(df, prob=prob)
        df = udata.filtrarPorTamanhoArray(df, tamanho=size)
        salvar(df=df, prob=prob, size=size)

