import os
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

import matplotlib.pyplot as plt

import util_ler_dados as udata
import util_graficos as graf

import seaborn as sns
plt.style.use('seaborn-whitegrid')

path_arq_destino = '03-Anova-2'

# def gerarGraficosQQPlot(ind_graf, col_desc, df_bubble, df_insertion, df_merge, df_quick, arq_destino):
def gerarGraficosQQPlot(ind_graf, ax, col_desc, algoritmo, data):

    ax = plt.subplot(2,2,ind_graf)
    plt.title('%s - %s' % (algoritmo, col_desc))
    graf.gerarQQPlot(ax=ax, data=data)


def gerarGraficosBoxPlot(ax, col, col_desc, dfs):
    data = pd.DataFrame()
    for df in dfs:
        data = data.append(other=df)

    plt.title('%s' % (col_desc))
    sns.boxplot(data=data, x='algoritmo', y=col, ax=ax)




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



colunas_desc={'largest_sorted_subarray':'maior_array',
              'percentual_maior_array':'maior_array_percentual',
              'k_unordered_sequence':'desordenados',
              'percentual_k_unordered':'desordenados_percentual'}


for prob in udata.PROBABILIDADES:
    for size in udata.TAMANHOS:
        df = udata.obterDados2()
        df = udata.filtrarPorProbabilidadeErro(df, prob=prob)
        df = udata.filtrarPorTamanhoArray(df, tamanho=size)

        if (df.shape[0] > 0):

            arq_name = 'anova_prob_%s_tam_%s' % (prob, size)
            arq_destino = os.path.join(path_arq_destino, '%s.txt' % (arq_name))
            if os.path.exists(arq_destino):
                os.remove(arq_destino)
            arq_destino = open(arq_destino, 'w+')

            csv_destino = os.path.join(path_arq_destino, 'csv/%s' % (arq_name))

            head_n = 1000
            df_bubble = df[df['algoritmo'] == 'bubble']#.head(head_n)
            df_merge = df[df['algoritmo'] == 'merge']#.head(head_n)
            df_insertion = df[df['algoritmo'] == 'insertion']#.head(head_n)
            df_quick = df[df['algoritmo'] == 'quick']#.head(head_n)

            print('=================================================================')
            print('Probabilidade = %s / Tamanho = %s' % (prob, size))
            print('=================================================================')

            for col in udata.COLUNAS_DEPENDENTES:
                df_dados_csv = pd.DataFrame()
                df_b = pd.DataFrame(df_bubble[col].reset_index())
                df_i = pd.DataFrame(df_insertion[col].reset_index())
                df_m = pd.DataFrame(df_merge[col].reset_index())
                df_q = pd.DataFrame(df_quick[col].reset_index())

                df_dados_csv = df_b.join(other=df_i[col], rsuffix='_insertion')
                df_dados_csv = df_dados_csv.join(other=df_m[col], rsuffix='_merge')
                df_dados_csv = df_dados_csv.join(other=df_q[col], rsuffix='_quick', lsuffix='_bubble')

                # df_dados_csv.rename(str.upper, axis='columns')
                df_dados_csv = df_dados_csv.rename(columns={ '%s_bubble'%(col): 'bubble',
                                    '%s_insertion'%(col): 'insertion',
                                    '%s_merge'%(col): 'merge',
                                    '%s_quick'%(col): 'quick'
                                    })
                #remove a coluna INDEX
                df_dados_csv = df_dados_csv.drop(columns=['index'])

                df_dados_csv.to_csv('%s_%s.csv' % ( csv_destino, colunas_desc[col].upper()),
                                    sep=',',
                                    index=False )

                s = col.upper()
                print(s)
                arq_destino.write(s + '\n')

                s = '=' * len(col)
                print(s)
                arq_destino.write(s + '\n')


                printAnova(col, df_bubble, df_insertion, df_merge, df_quick, arq_destino)
                print('')
                arq_destino.write('\n')

                gerarGraficos = False

                if (gerarGraficos):
                    #gera os graficos de QQPlot
                    fig = plt.figure(figsize=[20, 19])
                    plt.rcParams.update({'font.size': 20})
                    plt.suptitle('QQPlot - Teste de Normalidade - Prob. Erro: %s - Tam. Array: %s' % (prob, size))
                    ax = plt.gca()
                    gerarGraficosQQPlot(1, ax, col, 'BUBBLE', df_bubble[col])
                    gerarGraficosQQPlot(2, ax, col, 'INSERTION', df_insertion[col])
                    gerarGraficosQQPlot(3, ax, col, 'MERGE', df_merge[col])
                    gerarGraficosQQPlot(4, ax, col, 'QUICK', df_quick[col])

                    fig.savefig('%s/graficos/qqplot/%s_%s.png' % (path_arq_destino, arq_name, colunas_desc[col].upper()),
                                bbox_inches='tight',
                                pad_inches=2)
                    plt.close(fig)

                    #gera os graficos de Boxplot
                    fig = plt.figure(figsize=[20, 15])
                    plt.rcParams.update({'font.size': 20})
                    plt.suptitle('BoxPlot - Teste de Normalidade - Prob. Erro: %s - Tam. Array: %s' % (prob, size))
                    ax = plt.gca()
                    dfs = [df_bubble, df_insertion, df_merge, df_quick]
                    gerarGraficosBoxPlot(ax, col, col, dfs)
                    fig.savefig('%s/graficos/boxplot/%s_%s_boxplot.png' % (path_arq_destino, arq_name, colunas_desc[col].upper()),
                                bbox_inches='tight',
                                pad_inches=2)
                    plt.close(fig)

            arq_destino.close()