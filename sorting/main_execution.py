import sys
import os


def main(sorting_alg, data_size, perc_rate, repetitions):
    inFile = '_data-' + perc_rate + '-' + data_size + '.in'
    path = os.getcwd() + '/data-' + perc_rate + '/' + sorting_alg + '/' + data_size
    for n in range(0, int(repetitions)):
        createDir(path, sorting_alg, data_size)
        os.system('./' + sorting_alg + ' < ' + inFile + ' > ' + path + '/data-' + data_size + '-' + str(n+1) + '.out ')

def createDir(path, sorting_alg, data_size):
    if os.path.isdir(path) == False:
        try:
            os.makedirs(path)
        except OSError as ose:
            print ("Creation of the directory failed %s", path)
            print (ose)
        else:
            print ("Successfully created the directory ")


#print(os.path.dirname(os.path.abspath(__file__)))
alg = [
    #'quick', 
    #'bubble', 
    'merge', 
    #'insertion'
    ]
perc_rate = [
    'normal',
    #'001',
    #'002',
    #'005'
]
d_size = [
    #'100',
    '1000',
    '10000'
    ]
repetitions = '3000'

print('Iniciando execucao...')
for n in alg:
    print('Algoritmo: ' + n)
    for p in perc_rate:
        print('% Rate: ' + p)
        for y in d_size:
            print('Data Size: ' + y)
            print('Repeticoes: ' + repetitions)
            main(n, y, p, repetitions)
print('Finalizando execucao...')
