import sys
import os


def main(sorting_alg, data_size, perc_rate, ind_arq):
    ind_arq = ('0%s' % (ind_arq))[-2:]
    d_size = ('00000%s' % (data_size))[-5:]

    inFile = 'data-in-%.4f-%s-%s.txt' % (perc_rate, d_size, ind_arq)
    # inFile = '%s_data-%.4f-%s.txt'%(ind_arq, perc_rate, data_size)
    if os.path.exists('data-in/%s'%inFile):
        # print(perc_rate, data_size, inFile)
        path = os.getcwd() + 'data-in/%s' %(inFile)
        print('        %s'%inFile)

        outFile = 'data-out-%.4f-%s-%s-%s.txt'%(perc_rate, d_size, sorting_alg, ind_arq)
        cmd = './%s < data-in/%s > data-out/%s' % (sorting_alg, inFile, outFile)
        # print(cmd)
        os.system(cmd)
    # else:
    #     print('nao existe: %s' % inFile)


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
                main(a, size, prob, ind_arq)

print('Finalizando execucao...')
