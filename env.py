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

class Positon(Mana):
    def __init__(self, name: str, width,hight,*args, **kwargs):
        self.name=name
        self.width=width
        self.hight=hight
    def get(x,y):
        return (x,y)
    def get_w_d(self):
        return (self.width,self.hight)


class NdMana(Mana):
    def __init__(self, width:int,hight:int, name = ["light","scent"],*args, **kwargs):
        self.env=np.ndarray((len(name),width,hight))
        self.name=[]

class Light(Mana):
    def __init__(self, name: str,width:int,hight:int, *args, **kwargs):
        self.name=name
        self.width=width
        self.hight=hight
        self.bias=self.generetor()
        y=np.linspace(np.linspace(0,0.5,self.hight),np.linspace(0.5,1,self.hight),self.width)
        self.glass=np.sin(y*np.pi)+np.sin(y[::-1][::]*np.pi)  #范围是[1,2]，平均值非1.5
        self.glass=self.glass/self.glass.mean()/2               #归一化使的平均值为0.5
        self.update()

    def generetor(self):
        if self.width%20==0 and self.hight%20==0:
            block=np.random.random((self.width//20,self.hight//20))
            env=np.ones((self.width,self.hight))
            for i in range(self.width//20):
                for j in range(self.hight//20):
                    for k in range(20):
                        env[i*20+k][j*20:j*20+20]*=block[i][j]
            return env
        else:
            raise Exception("世界宽高不满足为20的整数倍")

    def update(self):
        print("light has updated")
        self.env=np.random.random((self.width,self.hight))*0.1+self.bias*0.1+self.glass*0.802
        #self.env=(np.tanh(self.env)+1)/2
        #self.env=np.tanh(np.random.random((self.width,self.hight))+1)/2
    def get(self,x,y):
        return self.env[x][y]
    def get_view(self,xy:tuple,size)->np.ndarray:
        x=xy[0]
        y=xy[1]
        view= self.env[x-size:x+size,y-size:y+size]
        return view
    def get_all(self)->np.ndarray:
        return self.env
    def mean(self):
        return self.env.mean()
