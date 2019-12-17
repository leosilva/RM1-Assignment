import sys
import os


def main(sorting_alg, data_size, perc_rate, ind_arq):
    ind_arq = ('0%s' % (ind_arq))[-2:]
    d_size = ('00000%s' % (data_size))[-5:]

    inFile = 'data-in-%.4f-%s-%s.txt' % (perc_rate, d_size, ind_arq)
    if os.path.exists('data-in-2/%s'%inFile):
        print('        %s'%inFile)

        outFile = 'data-out-%.4f-%s-%s-%s.txt'%(perc_rate, d_size, sorting_alg, ind_arq)
        cmd = './%s < data-in-2/%s > data-out-2/%s' % (sorting_alg, inFile, outFile)
        # print(cmd)
        os.system(cmd)


alg = ['quick', 'bubble', 'merge', 'insertion']
perc_rates = [0.02, 0.05]
d_size = [100, 1000, 10000]

alg = ['quick', 'merge']
alg = [ 'quick']
perc_rates = [0.01]
d_size = [100]

repetitions = 30

print('Iniciando execucao...')
for a in alg:
    print('Algoritmo: ' + a)
    for prob in perc_rates:
        print('  Perc. Rate: %s' % prob)
        for size in d_size:
            print('    Data Size: %s' % size)
            for ind_arq in range(1, 31):
                main(a, size, prob, ind_arq)

print('Finalizando execucao...')
