import numpy as np

class Mana:
    def __init__(self,name:str,*args,**kwargs):
        pass
    def update(self):
        pass
    def get(self):
        raise Exception("不允许不定义使用Mana.get")
    def get_all(self)->np.ndarray:
        pass
    def get_view(self):
        pass