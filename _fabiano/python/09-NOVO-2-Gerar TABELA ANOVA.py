# import plotly.plotly as py
# import plotly.graph_objs as go
# from plotly.tools import FigureFactory as FF
import os
import sys
import numpy as np
import pandas as pd
import scipy
import scipy.stats as stats

import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import util_ler_dados as udata


df_tudo = udata.obterDados2()

arq_destino = '03-Anova-2/_ANOVA_TODAS_ANALISES.txt'
if os.path.exists(arq_destino):
    os.remove(arq_destino)
arq_destino = open(arq_destino, 'w+')

for prob in udata.PROBABILIDADES_2:
    for tam in udata.TAMANHOS:
        data = udata.obterDfPorProbTam2(prob=prob, tam=tam, df=df_tudo)
        # print(data.head())

        lm = ols(formula='percentual_k_unordered ~ algoritmo', data=data).fit()
        anova = sm.stats.anova_lm(lm, typ=2) # Type 2 ANOVA DataFrame

        tit = ' ANOVA para Probabilidade = %s e Tamanho = %s' % (prob, tam)
        hr = '=' * 60 #len(tit)
        anov = anova.head(10)

        s = '%s\n%s\n%s\n%s\n\n' %(hr,tit,hr,anov)
        arq_destino.write(s)
        print(s)

        #insere dados do Tete de Nomelidade
        s = '    * TESTE DE NORMALIDADE (SHAPIRO-WILK):\n'
        s += '      %s\n' % ('-' * (len(s)+6))
        for alg in udata.ALGORTIMOS:
            d = data[data['algoritmo'] == alg]['percentual_k_unordered']
            W, p_value = stats.shapiro(d)
            s += '        - %s: W = %0.6f / p_value = %.6f \n' % (alg.ljust(9), W, p_value)
        s += '\n'
        arq_destino.write(s)
        print(s)


#fecha arquivo
arq_destino.close()


# pr_f = anova['PR(>F)'].values[0]
# print( '%s  /  %.55f' % (pr_f, pr_f) )

