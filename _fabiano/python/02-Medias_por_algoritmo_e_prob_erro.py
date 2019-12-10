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


for prob in probs:
    data = df_tudo[df_tudo.probabilidade_erro == float(prob)]

    df_means = data.groupby(['size_of_array', 'algoritmo']).mean()
    df_std = data.groupby(['size_of_array', 'algoritmo']).std()
    df_min = data.groupby(['size_of_array', 'algoritmo']).min()
    df_max = data.groupby(['size_of_array', 'algoritmo']).max()

    indx = 1

    #se tiver dados no DF
    if (data.shape[0] > 0):
        # print(data.head())

        graf_title = 'Estatísticas por Algoritmo para Probabilidade de Erro %s' % (prob)
        file_title = 'Estatisticas_por_Algoritmo_Prob_%s' % (prob)

        fig = plt.figure(figsize=[larg_fig, alt_fig])
        plt.suptitle(graf_title + '\nBarplot / Média / Desvio Padrão / Mín. / Máx.', fontsize=30)
        plt.rcParams.update({'font.size': font_size})

        #grafico de barras para % Desordenados
        ax = plt.subplot(rows, cols, indx)
        graf.gerarBarplot(x='size_of_array',
                          y='percentual_k_unordered',
                          hue='algoritmo',
                          data=data,
                          title='% Desordenados',
                          palette=color_map)
        indx += 1

        #grafico de barras para % Maior Array
        ax = plt.subplot(rows, cols, indx)
        graf.gerarBarplot(x='size_of_array',
                          y='percentual_maior_array',
                          hue='algoritmo',
                          data=data,
                          title='% Maior Array',
                          palette=color_map)
        indx += 1

        # grafico de barras para a média das % Desordenados
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Média - percentual_k_unordered')
        data_graf = df_means['percentual_k_unordered'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a média das % Maior Array
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Média - percentual_maior_array')
        data_graf = df_means['percentual_maior_array'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Desordenados
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Desvio P. - percentual_k_unordered')
        data_graf = df_std['percentual_k_unordered'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Maior Array
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Desvio P. - percentual_maior_array')
        data_graf = df_std['percentual_maior_array'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Desordenados
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Mín. - percentual_k_unordered')
        data_graf = df_min['percentual_k_unordered'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Maior Array
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Mín. - percentual_maior_array')
        data_graf = df_min['percentual_maior_array'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Desordenados
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Máx. - percentual_k_unordered')
        data_graf = df_max['percentual_k_unordered'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        # grafico de barras para a std_dev das % Maior Array
        ax = plt.subplot(rows, cols, indx)
        plt.ylabel('Máx. - percentual_maior_array')
        data_graf = df_max['percentual_maior_array'].unstack()
        data_graf.plot(kind='bar', ax=ax, color=color_map)
        indx += 1

        #salva o gráfico
        plt.savefig('graficos/comparacao_entre_algoritmos/%s.png' % (file_title), bbox_inches='tight', pad_inches=2)  # , format='png', orientation='landscape', papertype='letter')
