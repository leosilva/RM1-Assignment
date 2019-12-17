#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_graficos as graf

PROBABILIDADES = ['0.01', '0.02', '0.05', '0.001', '0.0001']

TAMANHOS = [100, 1000, 10000]

ALGORTIMOS = ['bubble', 'merge', 'quick', 'insertion']

COLUNAS_DEPENDENTES = ['largest_sorted_subarray','percentual_maior_array','k_unordered_sequence','percentual_k_unordered']

COLUNA_MAIOR_ARRAY = COLUNAS_DEPENDENTES[0]
COLUNA_MAIOR_ARRAY_PERCENTUAL = COLUNAS_DEPENDENTES[1]
COLUNA_DESORDENADOS = COLUNAS_DEPENDENTES[2]
COLUNA_DESORDENADOS_PERCENTUAL = COLUNAS_DEPENDENTES[3]

def obterDados2():
    csv = 'data-csv-2/dados_extraidos-2.csv'
    df_tudo = pd.read_csv(delimiter=';', filepath_or_buffer=csv)
    return df_tudo

def obterDados():
    csv = 'data-csv/dados_extraidos.csv'
    df_tudo = pd.read_csv(delimiter=';', filepath_or_buffer=csv)
    return df_tudo

    # pasta_origem = 'data-csv'
    # df_tudo = pd.DataFrame()
    #
    # for prob in probs:
    #     for size in sizes:
    #         filtro_arq = '%s_%s_' % (prob, size)
    #
    #         arqs_in = os.listdir(pasta_origem)
    #         for f in arqs_in:
    #             if (f.startswith(filtro_arq)):
    #                 # print(filtro_arq)
    #                 csv = os.path.join(pasta_origem, f)
    #                 df_tudo = df_tudo.append( pd.read_csv(delimiter=';', filepath_or_buffer=csv) )
    #
    # return df_tudo


def filtrarPorProbabilidadeErro(df, prob):
    if (type(prob) != float):
        prob = float(prob)

    return df[df.probabilidade_erro == prob]

def filtrarPorAlgoritmo(df, algoritmo):
    return df[df.algoritmo == algoritmo]

def filtrarPorTamanhoArray(df, tamanho):
    return df[df['size_of_array'] == tamanho]


def obterEstatisticasPorTamanho_Algoritmo(df):
    df_means = df.groupby(['size_of_array', 'algoritmo']).mean()
    df_std = df.groupby(['size_of_array', 'algoritmo']).std()
    df_min = df.groupby(['size_of_array', 'algoritmo']).min()
    df_max = df.groupby(['size_of_array', 'algoritmo']).max()
    df_var = df.groupby(['size_of_array', 'algoritmo']).var()
    return df_means, df_std, df_min, df_max, df_var