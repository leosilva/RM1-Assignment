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


data = udata.obterDados2()

arq_destino = '03-Anova-2/_ANOVA_TODAS_ANALISES_2_Fatores_com_Repeticao-[Tam-Prob-Alg].txt'
if os.path.exists(arq_destino):
    os.remove(arq_destino)
arq_destino = open(arq_destino, 'w+')

lm = ols(formula='percentual_k_unordered ~ algoritmo * probabilidade_erro * size_of_array', data=data).fit()
anova = sm.stats.anova_lm(lm, typ=2)

tit = ' ANOVA para ALgoritmo X Tamanho X Probabilidade'
hr = '=' * 60 #len(tit)
anov = anova.head(10)

s = '%s\n%s\n%s\n%s\n\n' %(hr,tit,hr,anova.to_string())
arq_destino.write(s)
print(s)


#fecha arquivo
arq_destino.close()

