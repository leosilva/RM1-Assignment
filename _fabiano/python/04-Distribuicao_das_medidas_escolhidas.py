#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_graficos as graf

# %matplotlib inline

# ========================================================
# estilos de graficos :
# >>  https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
# ========================================================
# plt.style.use('seaborn-whitegrid')
# plt.style.use('seaborn-pastel')
# plt.style.use('seaborn-colorblind')
# plt.style.use('seaborn-bright')
# plt.style.use('grayscale')
# plt.style.use('ggplot')
# plt.style.use('fivethirtyeight')
# plt.style.use('dark_background')
# plt.style.use('classic')
# plt.style.use('bmh')



pasta_origem = '../data/data_grouped'
arq_metadata = open('%s/_metadata.csv' % (pasta_origem), 'w+')

probs = ['0.01','0.02','0.05','0.001','0.0001']
# probs = ['0.01']#,'0.02']#,'0.05','0.001','0.0001']

sizes = ['100','1000','10000']

df_tudo = pd.DataFrame()

#le os arquivos de entrada
for prob in probs:
    for size in sizes:
        filtro_arq = '%s_%s_' % (prob, size)

        arqs_in = os.listdir(pasta_origem)
        for f in arqs_in:
            if (f.startswith(filtro_arq)):
                print(f)
                csv = os.path.join(pasta_origem, f)
                df_temp = pd.read_csv(delimiter = ';', filepath_or_buffer = csv)
                df_tudo = df_tudo.append(df_temp)

#ordena os registros por algoritmo
df_tudo.sort_values(by=['size_of_array','algoritmo'], inplace=True, ascending=[True,True])


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
    data = df_tudo[df_tudo.probabilidade_erro == float(prob)]

    group_by = ['probabilidade_erro', 'algoritmo']
    df_means = data.groupby(group_by).mean()
    df_std = data.groupby(group_by).std()
    df_min = data.groupby(group_by).min()
    df_max = data.groupby(group_by).max()

    # colunas_join = ['largest_sorted_subarray','k_unordered_sequence','percentual_k_unordered','percentual_maior_array']
    colunas_join = ['percentual_k_unordered','percentual_maior_array']
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
            df_dados_csv.to_csv('graficos/comparacao_entre_algoritmos/csv/%s.csv' % (file_title))

        if (gerar_graficos):
            graf_title = 'Estatísticas por Algoritmo Juntando Todos os Tamanhos - Probabilidade de Erro %s' % (prob)

            fig = plt.figure(figsize=[larg_fig, alt_fig])
            plt.suptitle(graf_title + '\nBarplot / Média / Desvio Padrão / Mín. / Máx.', fontsize=30)
            plt.rcParams.update({'font.size': font_size})

            #grafico de barras para % Desordenados
            ax = plt.subplot(rows, cols, indx)
            graf.gerarBarplot(ax=ax, x='probabilidade_erro',
                              y='percentual_k_unordered',
                              hue='algoritmo',
                              data=data,
                              title='% Desordenados',
                                  palette=color_map)
            graf.inserirValoresNasBarras(ax, df_means['percentual_k_unordered'] )
            indx += 1

            #grafico de barras para % Maior Array
            ax = plt.subplot(rows, cols, indx)
            graf.gerarBarplot(ax=ax, x='probabilidade_erro',
                              y='percentual_maior_array',
                              hue='algoritmo',
                              data=data,
                              title='% Maior Array',
                              palette=color_map)
            graf.inserirValoresNasBarras(ax, df_means['percentual_maior_array'].values)
            indx += 1

            # grafico de barras para a média das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Média - percentual_k_unordered')
            data_graf = df_means['percentual_k_unordered'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_means['percentual_k_unordered'].values)
            indx += 1

            # grafico de barras para a média das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Média - percentual_maior_array')
            data_graf = df_means['percentual_maior_array'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_means['percentual_maior_array'].values)
            indx += 1

            # grafico de barras para a std_dev das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Desvio P. - percentual_k_unordered')
            data_graf = df_std['percentual_k_unordered'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_std['percentual_k_unordered'].values)
            indx += 1

            # grafico de barras para a std_dev das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Desvio P. - percentual_maior_array')
            data_graf = df_std['percentual_maior_array'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_std['percentual_maior_array'].values)
            indx += 1

            # grafico de barras para a std_dev das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Mín. - percentual_k_unordered')
            data_graf = df_min['percentual_k_unordered'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_min['percentual_k_unordered'].values)
            indx += 1

            # grafico de barras para a std_dev das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Mín. - percentual_maior_array')
            data_graf = df_min['percentual_maior_array'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_min['percentual_maior_array'].values)
            indx += 1

            # grafico de barras para a std_dev das % Desordenados
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Máx. - percentual_k_unordered')
            data_graf = df_max['percentual_k_unordered'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_max['percentual_k_unordered'].values)
            indx += 1

            # grafico de barras para a std_dev das % Maior Array
            ax = plt.subplot(rows, cols, indx)
            plt.ylabel('Máx. - percentual_maior_array')
            data_graf = df_max['percentual_maior_array'].unstack()
            data_graf.plot(kind='bar', ax=ax, color=color_map)
            graf.inserirValoresNasBarras(ax, df_max['percentual_maior_array'].values)
            indx += 1

            #salva o gráfico
            plt.savefig('graficos/comparacao_entre_algoritmos/%s.png' % (file_title), bbox_inches='tight', pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
