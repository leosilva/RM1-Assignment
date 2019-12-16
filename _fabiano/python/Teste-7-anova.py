import os
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

import matplotlib.pyplot as plt

import util_ler_dados as udata
import util_graficos as graf

path_arq_destino = '../03-Anova'

# def gerarGraficosQQPlot(ind_graf, col_desc, df_bubble, df_insertion, df_merge, df_quick, arq_destino):
def gerarGraficosQQPlot(ind_graf, ax, col_desc, algoritmo, data):

    ax = plt.subplot(2,2,ind_graf)
    plt.title('%s - %s' % (algoritmo, col_desc))
    graf.gerarQQPlot(ax=ax, data=data)

    # ax = plt.subplot(2,2,2)
    # plt.title('% Desordenados (KDE)')
    # graf.gerarQQPlot(ax, df_bubble)
    #
    # ax = plt.subplot(2,2,3)
    # plt.title('% Maior Array')
    # graf.gerarQQPlot(ax, df_bubble)
    #
    # ax = plt.subplot(2,2,4)
    # plt.title('% Maior Array (KDE)')
    # graf.gerarQQPlot(ax, df_bubble)



def printShapiroTest(data, desc, arq_destino):
    W, p_value = stats.shapiro(data)
    s = '        - %s: W = %0.6f / p_value = %.6f' % (desc, W, p_value)
    print(s)
    arq_destino.write(s+'\n')
    return W, p_value



def printAnova(col, df_bubble, df_insertion, df_merge, df_quick, arq_destino):

    s = '    * TESTE DE NORMALIDADE (SHAPIRO-WILK):'
    print(s)
    arq_destino.write(s+'\n')

    s = '      -----------------------------------'
    print(s)
    arq_destino.write(s + '\n')


    printShapiroTest(df_bubble[col], 'BUBBLE'.ljust(9), arq_destino)
    printShapiroTest(df_insertion[col], 'INSERTION'.ljust(9), arq_destino)
    printShapiroTest(df_merge[col], 'MERGE'.ljust(9), arq_destino)
    printShapiroTest(df_quick[col], 'QUICK'.ljust(9), arq_destino)
    print('')
    arq_destino.write('\n')

    f_statistic, p_value = stats.f_oneway(
                                          df_bubble[col],
                                          df_insertion[col],
                                          df_merge[col],
                                          df_quick[col]
                                          )
    s = '    * ANOVA:'
    print(s)
    arq_destino.write(s+'\n')

    s = '      -----'
    print(s)
    arq_destino.write(s + '\n')

    s = '        - f_statistic = %.15f / p_value = %.15f' % (f_statistic, p_value)
    print(s)
    arq_destino.write(s+'\n')


for prob in udata.PROBABILIDADES:
    for size in udata.TAMANHOS:
        df = udata.obterDados(probs=[prob], sizes=[size])

        if (df.shape[0] > 0):

            arq_name = 'anova_prob_%s_tam_%s' % (prob, size)
            arq_destino = os.path.join(path_arq_destino, '%s.txt' % (arq_name))
            if os.path.exists(arq_destino):
                os.remove(arq_destino)
            arq_destino = open(arq_destino, 'w+')

            df_bubble = df[df['algoritmo'] == 'bubble']
            df_merge = df[df['algoritmo'] == 'merge']
            df_insertion = df[df['algoritmo'] == 'insertion']
            df_quick = df[df['algoritmo'] == 'quick']

            print('=================================================================')
            print('Probabilidade = %s / Tamanho = %s' % (prob, size))
            print('=================================================================')

            for col in udata.COLUNAS_DEPENDENTES:
                s = col.upper()
                print(s)
                arq_destino.write(s + '\n')

                s = '=' * len(col)
                print(s)
                arq_destino.write(s + '\n')


                printAnova(col, df_bubble, df_insertion, df_merge, df_quick, arq_destino)
                print('')
                arq_destino.write('\n')



                #gera os graficos de QQPlot
                fig = plt.figure(figsize=[20, 15])
                plt.suptitle('QQPlot - Teste de Normalidade - Prob. Erro: %s - Tam. Array: %s' % (prob, size))
                ax = plt.gca()
                gerarGraficosQQPlot(1, ax, col, 'BUBBLE', df_bubble[col])
                gerarGraficosQQPlot(2, ax, col, 'INSERTION', df_insertion[col])
                gerarGraficosQQPlot(3, ax, col, 'MERGE', df_merge[col])
                gerarGraficosQQPlot(4, ax, col, 'QUICK', df_quick[col])

                fig.savefig('%s/graficos/%s_%s.png' % (path_arq_destino, arq_name, col.upper()),
                            bbox_inches='tight',
                            pad_inches=2)
                plt.close(fig)

            arq_destino.close()