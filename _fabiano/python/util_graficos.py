# imports
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

import numpy as np
import pandas as pd

import seaborn as sns
from statsmodels.graphics.gofplots import qqplot


def gerarQQPlot(ax, data, line='s'):
    fig = qqplot(ax=ax, data=data, line=line)
    return fig


def gerarBarplot(ax, data, x, y, hue, title='', order=None, palette='Blues'):
    #retorna objeto 'ax'
    sns.barplot(ax=ax,
                x=x,
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

    return ax

def inserirValoresNasBarras(ax, values):
    rects = ax.patches
    labels = ["%.2f" % i for i in values]
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.0, height * 1.01, label, ha='center', va='bottom')

def inserirValoresNoBarplot(ax):
    rects = ax.patches
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.0, height * 1.01, '%.2f'%(height), ha='center', va='bottom')
