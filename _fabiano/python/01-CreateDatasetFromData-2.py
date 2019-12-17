import sys
import os
import shutil
import datetime
import time


def calcular_k_unordered_sequence(data):
    arr = data.split(' ')
    #
    indice1 = 0
    indice2 = 1
    indice_max = len(arr) - 1
    k = 0
    #
    while (indice1 < indice_max):
        #
        if (int(arr[indice1]) > int(arr[indice2])):
            k += 1
        #
        indice1 += 1
        indice2 += 1
    #
    return k

def main(algoritmo, data_size, prob_erro, ind_arq, arq_destino):
    ind_arq = ('0%s' % (ind_arq))[-2:]
    d_size = ('00000%s' % (data_size))[-5:]

    outFile = 'data-out-%.4f-%s-%s-%s.txt' % (prob_erro, d_size, algoritmo, ind_arq)

    if os.path.exists('data-out-2/%s'%outFile):
        print('        %s'%outFile)

        # le o arquivo .OUT
        file = open('data-out-2/%s'%outFile, 'r')
        # obtem os dados de cada uma das 4 linhas
        lines = file.readlines()
        l1_original_array = lines[0]
        l2_sorting_with_fault = lines[1]
        l3_sorting_ok = lines[2]
        l4_largest_sorted_subarray = int(lines[3])

        # se for a prob. erro default (1/n) ajusta a descricao no arquivo
        prob_erro_csv = prob_erro

        # calcula o percentual do maior array
        percentual_maior_array = 100.0 * int(l4_largest_sorted_subarray) / int(data_size)

        #
        k_unordered_sequence = calcular_k_unordered_sequence(l2_sorting_with_fault)
        #
        percentual_k_unordered = 100.0 * int(k_unordered_sequence) / int(data_size)
        #
        arq_destino.write('%s;%s;%s;%s;%s;%.2f;%.2f\n' % (
        algoritmo, prob_erro_csv, data_size, l4_largest_sorted_subarray, k_unordered_sequence, percentual_k_unordered,
        percentual_maior_array))


# define as pastas contendo os dados
pasta_origem = 'data-out-2'
pastas = os.listdir(pasta_origem)

#abre o arquivo onde serao salvos os dados extraidos
#se o arquivo ja existir, entao apaga e cria novamente
path_arq_destino = 'data-csv-2/dados_extraidos-2.csv'
if os.path.exists(path_arq_destino):
    os.remove(path_arq_destino)

arq_destino = open(path_arq_destino, 'w+')
arq_destino.write('%s;%s;%s;%s;%s;%s;%s\n' % ('algoritmo', 'probabilidade_erro', 'size_of_array', 'largest_sorted_subarray', 'k_unordered_sequence', 'percentual_k_unordered', 'percentual_maior_array') )



alg = ['quick','bubble','merge','insertion']
perc_rate = [0.01, 0.02, 0.05]
d_size = [100, 1000, 10000]

# perc_rate = [0.05]
# d_size = [1000]
#
repetitions = 30


print('Iniciando execucao...')
for a in alg:
    print('Algoritmo: ' + a)
    for prob in perc_rate:
        print('  Perc. Rate: %s' % prob)
        for size in d_size:
            print('    Data Size: %s' % size)
            for ind_arq in range(1, 31):
                main(a, size, prob, ind_arq, arq_destino)

