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

arq_destino = '03-Anova-2/_ANOVA_ANALISES_Probabilidades_de_um_mesmo_Algoritmo.txt'
if os.path.exists(arq_destino):
    os.remove(arq_destino)
arq_destino = open(arq_destino, 'w+')

for alg in udata.ALGORTIMOS:
    data = udata.filtrarPorAlgoritmo(df=df_tudo, algoritmo=alg)
    # print(data.head())
    print(data['probabilidade_erro'].unique())

    lm = ols(formula='percentual_k_unordered ~ probabilidade_erro', data=data).fit()
    anova = sm.stats.anova_lm(lm, typ=2) # Type 2 ANOVA DataFrame

    tit = ' ANOVA para %s' % (alg.upper())
    hr = '=' * 70 #len(tit)
    anov = anova.head(10)

    s = '%s\n%s\n%s\n%s\n\n' %(hr,tit,hr,anov)
    arq_destino.write(s)
    print(s)

    #insere dados do Tete de Nomelidade
    s = '    * TESTE DE NORMALIDADE (SHAPIRO-WILK):\n'
    s += '      %s\n' % ('-' * (len(s)+6))
    d = data['percentual_k_unordered']
    W, p_value = stats.shapiro(d)
    s += '        - Todas as Probabilidades %s: W = %0.6f / p_value = %.6f \n' % (d.shape[0], W, p_value)
    s += '\n'
    arq_destino.write(s)
    print(s)

    # #insere dados do Tete de Nomelidade
    # s = '    * TESTE DE NORMALIDADE (SHAPIRO-WILK):\n'
    # s += '      %s\n' % ('-' * (len(s)+6))
    # for prob in udata.PROBABILIDADES_2:
    #     d = data[data['probabilidade_erro'] == prob]['percentual_k_unordered']
    #     W, p_value = stats.shapiro(d)
    #     s += '        -> %s: W = %0.6f / p_value = %.6f \n' % (str(prob).ljust(6), W, p_value)
    # s += '\n'
    # arq_destino.write(s)
    # print(s)


#fecha arquivo
arq_destino.close()
