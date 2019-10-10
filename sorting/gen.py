from random import *

n_sizes = [100, 1000, 10000]
#n_sizes = [1, 2, 3]

for n in n_sizes:
    eps = 1.0/n
    maxr = n/2
    arq = "_data-%s.in"%(n)
    f = open(arq,"w")
    f.write(str(eps) + " " + str(n))
    for i in range(n):
        f.write(" " + str(randint(1,maxr)))
    f.write("\n")
    f.close()

# ============================
# CODIGO ANTERIOR
# ============================
# n = 10000
# eps = 1.0/n
# maxr = n/2

# f = open("data2.in","w")
# f.write(str(eps) + " " + str(n))

# for i in range(n):
#     f.write(" " + str(randint(1,maxr)))
# f.write("\n")

# f.close()

