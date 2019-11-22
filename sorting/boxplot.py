import pandas as pd
import re
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

perc_rate = [
    'normal',
    '001',
    '002',
    '005'
]
d_size = ['100', '1000', '10000']

for p in perc_rate:
    print("% Rate: " + p)
    for d in d_size:
        print("Size: " + d)
        data = pd.read_csv('_data-' + p + '-' + d + '.csv', sep=',', encoding='utf-8')
        print("Mean: "+ str(data.number.mean()))
        print("Standard Deviation: "+ str(data.number.std()))
        print("Describe:")
        print(str(data.number.describe()))

        # Histogram
        plt.figure(figsize=(8, 6))
        plt.hist(data.number, bins=15)
        plt.title('Numbers')
        plt.xlabel('Number')
        plt.ylabel('Frequency')
        plt.savefig('histogram-' + p + '-' + d + '.png')
        plt.close()

        # Boxplot
        data.boxplot()
        plt.title('Sample Array - ' + p + '% - ' + d + ' Elements') 
        plt.ylabel('Number')
        plt.savefig('boxplot-' + p + '-' + d + '.png')
        plt.close()