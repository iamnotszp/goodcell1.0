import torch
import torch.nn as nn
import torch.random as random
import numpy as np
from torchvision.transforms import ToTensor
class Soul:
    def __init__(self, observation_space, action_space,model):
        self.observation_space=observation_space
        self.action_space = action_space
        if model!=None:
            self.model=model
        else:
            self.model = nn.Sequential(
            nn.Linear(len(self.observation_space), 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24,len(action_space))
        )

    def think(self, state:np.ndarray):
        state=torch.Tensor(state)
        with torch.no_grad():   #无需反向传播
            q_values=self.model.forward(state)      #获得模型的Q估计
        #q_values = 1 if self.model.forward(torch.tensor(state)) > 0.5 else 0
        #return q_values
        return int(torch.argmax(q_values))       #选择Q估计最大的动作
    
    def copy_m(self):
        model=torch.view_copy(self.model)
        return Soul(self.observation_space,self.action_space,model)
    def mutate(self,model:nn.Module,pate:float):
        for i in self.model.parameters:
            i+=torch.rand((1))*pate

class SoulPool():
    i=0
    def __init__(self):
        self.map=[]

    def get_one(self,*args,**kwargs):
        pass
