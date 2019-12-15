#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd
import scipy.stats

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_ler_dados as udata

def mean_confidence_interval(data, confidence):
    decimais = 4

    prob_inv_cumul = {0.99: 2.576, 0.98: 2.326, 0.95: 1.960, 0.90: 1.645}

    k = prob_inv_cumul[confidence]

    a = 1.0 * np.array(data)
    n = len(a)

    mean, std_error, std_dev = np.mean(a), scipy.stats.sem(a), np.std(a)

    mean = np.round(mean, decimais)
    std_error = np.round(std_error, decimais)
    std_dev = np.round(std_dev, decimais)

    h = k * std_error
    h = np.round(h, decimais)

    lim_inferior = np.round(mean-h, decimais)
    lim_superior = np.round(mean+h, decimais)

    return lim_inferior, mean, lim_superior, h, std_error, std_dev

def printInfo(lim_inferior, mean, lim_superior, h, std_error, std_dev):
    s = '%.4f ≤ µ ≤ %.4f  media=%.4f   h=%.4f    std_error=%.4f    std_dev=%.4f' % (lim_inferior, lim_superior, mean, h, std_error, std_dev)
    return s

def printCsvInfo(coef_conf, prob, size, alg, coluna, lim_inferior, mean, lim_superior, h, std_error, std_dev):
    s = '%s;%s;%s;%s;%s;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f\n' % (coluna, coef_conf, prob, size, alg, lim_inferior, mean, lim_superior, std_error, h, std_dev)
    return s



path_arq_destino = '../02-Estatisticas/_confidence_intervals.txt'
if os.path.exists(path_arq_destino):
    os.remove(path_arq_destino)
arq_destino = open(path_arq_destino, 'w+')


probs = udata.PROBABILIDADES
sizes = udata.TAMANHOS
algs  = udata.ALGORTIMOS
# probs = [0.05]
# sizes = [100]
# algs  = ['bubble']

coeficientes_confianca = [0.99, 0.98, 0.95, 0.90]

colunas=['largest_sorted_subarray','percentual_maior_array','k_unordered_sequence','percentual_k_unordered']
colunas_desc=['maior_array','percentual_maior_array','desordenados','percentual_desordenados']

df = udata.obterDados()

for i in range(0, len(colunas)):
    col = colunas[i]
    col_desc = colunas_desc[i]
    path_arq_csv_destino = '../02-Estatisticas/_confidence_intervals_%s.csv' %(col_desc)
    if os.path.exists(path_arq_csv_destino):
        os.remove(path_arq_csv_destino)
    arq_csv_destino = open(path_arq_csv_destino, 'w+')
    arq_csv_destino.write('coluna;coef_confianca;probabilidade_err;tamanho_array;algoritmo;lim_inferior;media;lim_superior;std_error;h;std_dev\n')

    for coef in coeficientes_confianca:
        arq_destino.write('=============================================================================\n')
        arq_destino.write('Coeficiente de Confiança = %s\n' % (coef))
        arq_destino.write('=============================================================================\n')
        arq_destino.write('\n')

        for prob in probs:
            df_prob = udata.filtrarPorProbabilidadeErro(df, prob)
            for size in sizes:
                df_size = udata.filtrarPorTamanhoArray(df_prob, size)
                for alg in algs:
                    df_alg = udata.filtrarPorAlgoritmo(df_size, alg)
                    if (df_alg.shape[0]> 0):
                        arq_destino.write(col)
                        arq_destino.write('\n')
                        arq_destino.write('Coef. Confiança = %s;  Prob = %s;  Size = %s;  Alg = %s' % (coef, prob, size, alg))
                        arq_destino.write('\n')

                        data = df_alg[col]
                        lim_inferior, mean, lim_superior, h, std_error, std_dev = mean_confidence_interval(data, confidence=coef)
                        arq_csv_destino.write(printCsvInfo(coef, prob, size, alg, col, lim_inferior, mean, lim_superior, h, std_error, std_dev))

                        arq_destino.write(printInfo(lim_inferior, mean, lim_superior, h, std_error, std_dev))
                        arq_destino.write('\n\n')

                        # coluna = 'percentual_maior_array'
                        # data = df[coluna]
                        # lim_inferior, mean, lim_superior, h, std_error = mean_confidence_interval(data, confidence=coef)
                        # arq_csv_destino.write(printCsvInfo(coef, prob, size, alg, coluna, lim_inferior, mean, lim_superior, h, std_error))
                        #
                        # arq_destino.write(coluna)
                        # arq_destino.write('\n')
                        # arq_destino.write(printInfo(lim_inferior, mean, lim_superior, h, std_error))
                        # arq_destino.write('\n')

        arq_destino.write('\n\n')

