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


alg = ['quick','bubble','merge','insertion']
probs = [0.01, 0.02, 0.05]
sizes = [100, 1000, 10000]



csv = 'data-csv-2/dados_extraidos-2.csv'
df_tudo = udata.obterDados2()
# print(df_tudo)

#ordena os registros por algoritmo
df_tudo.sort_values(by=[udata.obterNomeColuna('size_of_array'),udata.obterNomeColuna('algoritmo')], inplace=True, ascending=[True,True])


# gera os graficos
rows = 5
cols = 2

larg_fig = 32
alt_fig  = 41
font_size = 15

sns_palette = 'Set2'
color_map = sns.color_palette(sns_palette, n_colors=4)

gerar_graficos = True
gerar_csvs_com_dados_dos_graficos = True

df_dados_csv = pd.DataFrame()

for prob in probs:
    data = df_tudo[df_tudo[udata.obterNomeColuna('probabilidade_erro')] == float(prob)]

    group_by = [udata.obterNomeColuna('probabilidade_erro'), udata.obterNomeColuna('algoritmo')]
    df_means = data.groupby(group_by).mean()
    df_std = data.groupby(group_by).std()
    df_min = data.groupby(group_by).min()
    df_max = data.groupby(group_by).max()

    # colunas_join = ['largest_sorted_subarray','k_unordered_sequence',udata.obterNomeColuna('percentual_k_unordered'),udata.obterNomeColuna('percentual_maior_array')]
    colunas_join = [udata.obterNomeColuna('percentual_k_unordered'),udata.obterNomeColuna('percentual_maior_array')]
    df_dados_csv = df_means[colunas_join]
    df_dados_csv = df_dados_csv.join(other=df_std[colunas_join], rsuffix='_std')
    df_dados_csv = df_dados_csv.join(other=df_min[colunas_join], rsuffix='_min')
    df_dados_csv = df_dados_csv.join(other=df_max[colunas_join], rsuffix='_max', lsuffix='_mean')

    indx = 1

    #se tiver dados no DF
    if (data.shape[0] > 0):
        # print(data.head())

        file_title = 'Estatisticas_por_Algoritmo_Juntando_os_Tamanhos_Prob_%s' % (prob)

        if (gerar_csvs_com_dados_dos_graficos):
            df_dados_csv.to_csv('../resultados/graficos-2/comparacao_entre_algoritmos/csv/%s.csv' % (file_title))

        if (gerar_graficos):
            graf_title = 'Estatísticas por Algoritmo Juntando Todos os Tamanhos - Probabilidade de Erro %s' % (prob)

            fig = plt.figure(figsize=[larg_fig, alt_fig])
            plt.suptitle(graf_title + '\nBarplot / Média / Desvio Padrão / Mín. / Máx.', fontsize=30)
            plt.rcParams.update({'font.size': font_size})

            #grafico de barras para % Desordenados
            ax = plt.subplot(rows, cols, indx)
            graf.gerarBarplot(ax=ax, x=udata.obterNomeColuna('probabilidade_erro'),
                              y=udata.obterNomeColuna('percentual_k_unordered'),
                              hue=udata.obterNomeColuna('algoritmo'),
                              data=data,
                              title=udata.obterNomeColuna('percentual_k_unordered'),#'% Desordenados',
                                  palette=color_map)
            graf.inserirValoresNasBarras(ax, df_means[udata.obterNomeColuna('percentual_k_unordered')] )
            indx += 1

            #grafico de barras para % Maior Array
            ax = plt.subplot(rows, cols, indx)
            graf.gerarBarplot(ax=ax,
                              x=udata.obterNomeColuna('probabilidade_erro'),
                              y=udata.obterNomeColuna('percentual_maior_array'),
                              hue=udata.obterNomeColuna('algoritmo'),
                              data=data,
                              title=udata.obterNomeColuna('percentual_maior_array'),#'% Maior Array',
                              palette=color_map)
            graf.inserirValoresNasBarras(ax, df_means[udata.obterNomeColuna('percentual_maior_array')].values)
            indx += 1

            # grafico de barras para a média das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Mean - %s'%(udata.obterNomeColuna('percentual_k_unordered')))
            data_graf = df_means[udata.obterNomeColuna('percentual_k_unordered')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_means[udata.obterNomeColuna('percentual_k_unordered')].values)
            indx += 1

            # grafico de barras para a média das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Mean - %s'%(udata.obterNomeColuna('percentual_maior_array')))
            data_graf = df_means[udata.obterNomeColuna('percentual_maior_array')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_means[udata.obterNomeColuna('percentual_maior_array')].values)
            indx += 1

            # grafico de barras para a std_dev das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Std.Dev. - %s'%(udata.obterNomeColuna('percentual_k_unordered')))
            data_graf = df_std[udata.obterNomeColuna('percentual_k_unordered')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_std[udata.obterNomeColuna('percentual_k_unordered')].values)
            indx += 1

            # grafico de barras para a std_dev das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Std.Dev. - %s'%(udata.obterNomeColuna('percentual_maior_array')))
            data_graf = df_std[udata.obterNomeColuna('percentual_maior_array')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_std[udata.obterNomeColuna('percentual_maior_array')].values)
            indx += 1

            # grafico de barras para a MIN das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Min. - %s'%(udata.obterNomeColuna('percentual_k_unordered')))
            data_graf = df_min[udata.obterNomeColuna('percentual_k_unordered')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_min[udata.obterNomeColuna('percentual_k_unordered')].values)
            indx += 1

            # grafico de barras para a MIN das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Min. - %s'%(udata.obterNomeColuna('percentual_maior_array')))
            data_graf = df_min[udata.obterNomeColuna('percentual_maior_array')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_min[udata.obterNomeColuna('percentual_maior_array')].values)
            indx += 1

            # grafico de barras para a MAX das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Max. - %s'%(udata.obterNomeColuna('percentual_k_unordered')))
            data_graf = df_max[udata.obterNomeColuna('percentual_k_unordered')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_max[udata.obterNomeColuna('percentual_k_unordered')].values)
            indx += 1

            # grafico de barras para a std_dev das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Max. - %s'%(udata.obterNomeColuna('percentual_maior_array')))
            data_graf = df_max[udata.obterNomeColuna('percentual_maior_array')].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_max[udata.obterNomeColuna('percentual_maior_array')].values)
            indx += 1

            #salva o gráfico
            plt.savefig('../resultados/graficos-2/comparacao_entre_algoritmos/%s.png' % (file_title), bbox_inches='tight', pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
