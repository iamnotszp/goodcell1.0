import numpy as np
from Object import Object
def gene_to_performance(gene:np.int128)->list:
    pass
def can_breed(object1:Object,object2:Object)->bool:
    return np.abs(object1.gene-object2.gene)<128