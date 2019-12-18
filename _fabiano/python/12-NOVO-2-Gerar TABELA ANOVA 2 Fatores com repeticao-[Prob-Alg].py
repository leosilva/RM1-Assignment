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

arq_destino = '03-Anova-2/_ANOVA_TODAS_ANALISES_2_Fatores_com_Repeticao-[Prob-Alg].txt'
if os.path.exists(arq_destino):
    os.remove(arq_destino)
arq_destino = open(arq_destino, 'w+')

for tam in udata.TAMANHOS:
    data = udata.obterDfPorTam2(tam=tam, df=df_tudo)
    # print(data.head())

    lm = ols(formula='percentual_k_unordered ~ algoritmo * probabilidade_erro', data=data).fit()
    anova = sm.stats.anova_lm(lm, typ=2) # Type 2 ANOVA DataFrame

    tit = ' ANOVA para Tamanho = %s ' % (tam)
    hr = '=' * 60 #len(tit)
    anov = anova.head(10)

    s = '%s\n%s\n%s\n%s\n\n' %(hr,tit,hr,anov)
    arq_destino.write(s)
    print(s)


#fecha arquivo
arq_destino.close()

