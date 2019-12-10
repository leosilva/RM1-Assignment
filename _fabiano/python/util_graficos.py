# imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns


def gerarBarplot(data, x, y, hue, title='', order=None, palette='Blues'):
    #retorna objeto 'ax'
    return sns.barplot(x=x,
                       y=y,
                       hue=hue,
                       data=data,
                       palette=palette,
                       order=order,
                       capsize=0.05,
                       saturation=8,
                       errcolor='gray',
                       errwidth=2,
                       ci='sd'
                       ).set_title(title)


