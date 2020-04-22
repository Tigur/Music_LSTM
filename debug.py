from model_run import i,o
import numpy as np


def give_shapes():

    return i.shape,o.shape

def decapsulate(i,depth=1):
    while(depth > 0):
        i = i[0]
        depth = depth - 1
    return i

print(give_shapes())
print(decapsulate(np.array(i),1))

print("WHOLE : ")
#print(np.array(i) )
