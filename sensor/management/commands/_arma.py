from numpy import append,array
from numpy.random import normal


def arma(n):
    sigma = 10
    init_length = 100
    phi = (0.5, 0.4)
    theta = (0.3, 0.3)
    
    w=normal(0 , sigma , n + init_length)
    ARMA=array([])
    s=0.0
    l = max(len(phi),len(theta))
    for i in range(n + init_length):
        if(i<l):
            ARMA=append(ARMA,w[i])
        else:
            s=0.0
            for j in range(len(phi)):
                s=s+phi[j]*ARMA[i-j-1]
            for j in range(len(theta)):
                s=s+theta[j]*w[i-j-1]

            ARMA=append(ARMA,s+w[i])

    return ARMA[init_length:]
