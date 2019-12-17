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

def mean_confidence_interval_distrib_T(data, confidence):
    decimais = 4

    # estes são só para N = 1000
    # prob_inv_cumul = {0.99: 2.330, 0.98: 2.056, 0.95: 1.646, 0.90: 1.282}

    # estes são só para N = 30
    prob_inv_cumul = {0.99: 2.457, 0.98: 2.147, 0.95: 1.697, 0.90: 1.310}

    k = prob_inv_cumul[confidence]

    a = 1.0 * np.array(data)

    n = len(a)
    v = n - 1 #calcula o grau de liberdade (letra grega "ni" que parece um "v")

    mean = np.mean(a)
    std_error = scipy.stats.sem(a)

    var_nao_tendenciosa = np.var(a, ddof=1)
    std_dev_nao_tendencioso = np.sqrt(var_nao_tendenciosa)

    mean = np.round(mean, decimais)
    std_error = np.round(std_error, decimais)
    std_dev = np.round(std_dev_nao_tendencioso, decimais)

    h = k * std_error
    h = np.round(h, decimais)

    lim_inferior = np.round(mean-h, decimais)
    lim_superior = np.round(mean+h, decimais)

    # print( lim_inferior, mean, lim_superior, h, std_error, std_dev)
    return lim_inferior, mean, lim_superior, h, std_error, std_dev

def printInfo(lim_inferior, mean, lim_superior, h, std_error, std_dev):
    s = '%.4f ≤ µ ≤ %.4f  media=%.4f   h=%.4f    std_error=%.4f    std_dev=%.4f' % (lim_inferior, lim_superior, mean, h, std_error, std_dev)
    return s

def printCsvInfo(coef_conf, prob, size, alg, coluna, lim_inferior, mean, lim_superior, h, std_error, std_dev):
    s = '%s;%s;%s;%s;%s;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f\n' % (coluna, coef_conf, prob, size, alg, lim_inferior, mean, lim_superior, std_error, h, std_dev)
    return s



path_arq_destino = '02-Estatisticas-2/interv_confianca_distrib_t/_intervalos_confianca_distrib_T.txt'
if os.path.exists(path_arq_destino):
    os.remove(path_arq_destino)
arq_destino = open(path_arq_destino, 'w+')


probs = udata.PROBABILIDADES
sizes = udata.TAMANHOS
algs  = udata.ALGORTIMOS
coeficientes_confianca = [0.99, 0.98, 0.95, 0.90]

# probs = [0.05]
# sizes = [100]
# algs  = ['bubble']
# coeficientes_confianca = [0.99]


colunas=['largest_sorted_subarray','percentual_maior_array','k_unordered_sequence','percentual_k_unordered']
colunas_desc=['maior_array','percentual_maior_array','desordenados','percentual_desordenados']

df = udata.obterDados2()

for i in range(0, len(colunas)):
    col = colunas[i]
    col_desc = colunas_desc[i]
    path_arq_csv_destino = '02-Estatisticas-2/interv_confianca_distrib_t/_intervalos_confianca_distrib_T_%s.csv' %(col_desc)
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
                        lim_inferior, mean, lim_superior, h, std_error, std_dev = mean_confidence_interval_distrib_T(data, confidence=coef)
                        arq_csv_destino.write(printCsvInfo(coef, prob, size, alg, col, lim_inferior, mean, lim_superior, h, std_error, std_dev))

                        arq_destino.write(printInfo(lim_inferior, mean, lim_superior, h, std_error, std_dev))
                        arq_destino.write('\n\n')

        arq_destino.write('\n\n')

