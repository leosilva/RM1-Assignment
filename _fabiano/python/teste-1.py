#imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
plt.style.use('seaborn-whitegrid')

import util_graficos as graf


pasta_origem = '../data/data_grouped'
arq_metadata = open('%s/_metadata.csv' % (pasta_origem), 'w+')

probs = ['0.01','0.02','0.05','0.001','0.0001']
probs = ['0.01']#,'0.02']#,'0.05','0.001','0.0001']
sizes = ['100','1000','10000']

df_tudo = pd.DataFrame()

for prob in probs:
    for size in sizes:
        filtro_arq = '%s_%s_' % (prob, size)

        arqs_in = os.listdir(pasta_origem)
        for f in arqs_in:
            if (f.startswith(filtro_arq)):
                csv = os.path.join(pasta_origem, f)
                df_temp = pd.read_csv(delimiter = ';', filepath_or_buffer = csv)
                df_tudo = df_tudo.append(df_temp)

#ordena os registros por algoritmo
df_tudo = df_tudo[['algoritmo','size_of_array', 'percentual_k_unordered','percentual_maior_array']]
df_tudo.sort_values(by=['size_of_array','algoritmo'], inplace=True, ascending=[True,True])

# print(df_tudo.head())

df_means = df_tudo.groupby(['size_of_array','algoritmo']).mean()
print(df_means.head())

data = df_means['percentual_k_unordered'].unstack()
print(data)

data.plot(kind='bar')
plt.show()


# print(data.columns)
# print(type(data))
# print(type(data['bubble']))
# data
#
# sns.lineplot(data=data )
# sns.barplot(data=data)
# plt.show()

# print (df_means.columns )
# print (df_means.unstack())
# print (df_means.head(20) )


# df_std = df_tudo.groupby(by='algoritmo').std()
# print (df_std.head() )
#
# df_median = df_tudo.groupby(by='algoritmo').median()
# print (df_median.head() )
#
# df_var = df_tudo.groupby(by='algoritmo').var()
# print (df_var.head() )
#
# df_min = df_tudo.groupby(by='algoritmo').min()
# print (df_min.head() )
#
# df_max = df_tudo.groupby(by='algoritmo').max()
# print (df_max.head() )


# data =df_means.unstack()
# print (data.columns, data.index )
# print (data.index['percentual_k_unordered'])
# sns.lineplot(x=df_means.unstack['size_of_array'], y=df_means.unstack['percentual_k_unordered'], data=df_means.unstack)
# sns.lineplot(x='algoritmo', y='percentual_k_unordered', hue='size_of_array', data=df_means.unstack() )
# plt.show()