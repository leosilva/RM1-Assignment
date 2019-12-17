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

    if os.path.exists('data-out/%s'%outFile):
        print('        %s'%outFile)

        # le o arquivo .OUT
        file = open('data-out/%s'%outFile, 'r')
        # obtem os dados de cada uma das 4 linhas
        lines = file.readlines()
        l1_original_array = lines[0]
        l2_sorting_with_fault = lines[1]
        l3_sorting_ok = lines[2]
        l4_largest_sorted_subarray = int(lines[3])

        # se for a prob. erro default (1/n) ajusta a descricao no arquivo
        prob_erro_csv = prob_erro
        # if (prob_erro == '1/n'):
        #     prob_erro_csv = '%g' % (1.0 / int(n))

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
pasta_origem = 'data-out'
pastas = os.listdir(pasta_origem)

#abre o arquivo onde serao salvos os dados extraidos
#se o arquivo ja existir, entao apaga e cria novamente
path_arq_destino = 'data-csv/dados_extraidos.csv'
if os.path.exists(path_arq_destino):
    os.remove(path_arq_destino)

arq_destino = open(path_arq_destino, 'w+')
arq_destino.write('%s;%s;%s;%s;%s;%s;%s\n' % ('algoritmo', 'probabilidade_erro', 'size_of_array', 'largest_sorted_subarray', 'k_unordered_sequence', 'percentual_k_unordered', 'percentual_maior_array') )

alg = [
    'quick',
    'bubble',
    'merge',
    'insertion'
    ]
perc_rate = [
    0.0100,
    0.0010,
    0.0001,
    #'001',
    #'002',
    #'005'
]
d_size = [
    100,
    1000,
    10000
    ]

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


#
#
# #
# for pasta_prob_erro in pastas:
#     #teste para não pegar a pasta ".DStore" do macOS
#     if (pasta_prob_erro[0] not in ['.','_']):
#         prob_erro = pasta_prob_erro.split('-')[1].replace(' div ', '/')
#         pastas_prob_erro = '%s/%s' % (pasta_origem, pasta_prob_erro)
#         pastas = os.listdir(pastas_prob_erro)
#         print('*processando: prob. erro = %s' % prob_erro)
#         #
#         for pasta_algoritmo in pastas:
#             # teste para não pegar a pasta ".DStore" do macOS
#             if (pasta_algoritmo[0] != '.'):
#                 algoritmo = pasta_algoritmo
#                 pastas_algoritmo = '%s/%s' % (pastas_prob_erro, pasta_algoritmo)
#                 # print(pastas_prob_erro,' || ', pastas_algoritmo)
#                 pastas = os.listdir(pastas_algoritmo)
#                 # print('    *processando: algoritmo = %s' % algoritmo)
#                 #
#                 for pasta_n in pastas:
#                     # teste para não pegar a pasta ".DStore" do macOS
#                     if (pasta_n[0] != '.'):
#                         n = pasta_n
#                         pastas_n = '%s/%s' % (pastas_algoritmo, pasta_n)
#                         pastas = os.listdir(pastas_n)
#                         # print(pastas_n)
#                         # print('        *processando: n = %s' % n)
#                         #
#                         for arq_out in pastas:
#                             # print('            *processando: arq = %s' % arq_out)
#                             arq = '%s/%s' % (pastas_n, arq_out)
#                             # print(arq)
#
#                             #le o arquivo .OUT
#                             file = open(arq, 'r')
#                             #obtem os dados de cada uma das 4 linhas
#                             lines = file.readlines()
#                             l1_original_array = lines[0]
#                             l2_sorting_with_fault = lines[1]
#                             l3_sorting_ok = lines[2]
#                             l4_largest_sorted_subarray = int(lines[3])
#
#                             #se for a prob. erro default (1/n) ajusta a descricao no arquivo
#                             prob_erro_csv = prob_erro
#                             if (prob_erro == '1/n'):
#                                 prob_erro_csv = '%g' % (1.0/int(n))
#
#
#                             #calcula o percentual do maior array
#                             percentual_maior_array = 100.0 * int(l4_largest_sorted_subarray) / int(n)
#
#                             #
#                             k_unordered_sequence = calcular_k_unordered_sequence(l2_sorting_with_fault)
#                             #
#                             percentual_k_unordered = 100.0 * int(k_unordered_sequence) / int(n)
#                             #
#                             arq_destino.write( '%s;%s;%s;%s;%s;%.2f;%.2f\n' % (algoritmo, prob_erro_csv, n, l4_largest_sorted_subarray, k_unordered_sequence, percentual_k_unordered, percentual_maior_array ))
#
#                             # break