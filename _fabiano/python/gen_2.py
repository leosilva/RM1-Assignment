from random import *

n_sizes = [100, 1000, 10000]
epss = [ 0.02, 0.05 ]

n_sizes = [100]
epss = [ 0.01 ]

for eps in epss:
    for n in n_sizes:
        for c in range(1,31):
            eps = eps
            maxr = n/2
            s1 = ('0%s'%(c))[-2:]
            s2 = str(eps).rjust(5)
            s3 = ('00000%s' % (n))[-5:]

            arq = "data-in-2/data-in-%.4f-%s-%s.txt"%(eps, s3, s1)
            print(arq)
            f = open(arq,"w")
            f.write(str(eps) + " " + str(n))
            for i in range(n):
                f.write(" " + str(randint(1,maxr)))
            f.write("\n")
            f.close()
