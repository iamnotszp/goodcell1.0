import pygame
import threading
import time
import random
import numpy as np
from pygame.rect import Rect
from pygame.sprite import Sprite
from soul import Soul
from env import Light,Positon

class Object(Sprite):
    def __init__(self,rect: Rect,gene:np.int64) -> None:
        self.rect=rect
        self.gene=gene
    def _mutate(self):
        pass
    def _move(self,move_avalible):
        pass
    def _think(self,view:np.ndarray):
        pass
    def _produce(self):
        pass
    def _act(self):
        pass
    def _born(self):
        pass
    def _die(self):
        pass
    def update(self):
        pass


class V(pygame.sprite.Sprite):
    i=1
    image=pygame.surfarray.make_surface(np.ones((2,2,3))*255)
    @staticmethod
    def _getid():
        V.i=V.i+1
        return V.i


    def __init__(self,soul:Soul,env,x=0,y=0,energe=0,speed=3) -> None:
        super().__init__()
        #self.image=pygame.image.load(face)
        if not env.get("space"):   
            raise Exception("错误，未设置space环境")
        self.env=env                #所处环境（供调用的api）
        self.age=0                  #当前寿命
        self.id=self._getid()       #一个特定标识
        self.action=0               #标识object目前的行动
        self.width,self.hight=self._getenv("space").get_w_d()       #最大宽高，用于objct.act和object.update()
        self.produce_rate=240       #生产效率（在1.0光照下能产生多少能量）
        self.constant_waste=100     #固定消耗（修正变量：防止摆烂，加速淘汰）
        self.light_waste=0.01       #每秒使得所在处（space(x,y))的光能减少多少）（修正变量：实现种间竞争）
        self.dead_energe=500        #小于多少能量下会死亡
        #可遗传量
        self.rect=pygame.rect.Rect(x,y,2,2)                         #自身的位置，之所以不放在env中主要是为了方便，#TODO：未来可能会放到object.state中
        self.image=V.image          #自己的图片，用于可视化  #TODO：将可视化与模拟分离
        self.action_space=range(5)  #动作空间
        self.observe_space=range(16)#观测空间
        self.speed=speed            #移动速度
        self.born_energe=6000       #判断什么时候生育
        self.max_age=15000          #最大寿命
        self.view_distance=2        #与神经网络的大小有关，目前无法改动
        self.energe=energe          #初始能量
        self.soul=soul              #object的大脑
    
    #获取自己所处的所有环境（的api）
    def _getenv_all(self):
        result=[]
        for key,val in self.env:
            result.append((key,val))
        return result

    #获得某个环境，如_getenv("light")
    def _getenv(self,name:str):
        return self.env.get(name)

    #死亡时自动调用的函数
    def die(self):
        #print(self.id,"is dying")
        if random.random()<0.05:
            print(self.id,"died")
            self.kill()
    #繁殖时调用函数
    def born(self):
        group=self.groups()[0]
        self.energe-=3000
        group.add(V(self.soul,self.env,random.randint(0,self.width-12)+5,random.randint(0,self.hight-12)+5))

    #模拟光和作用
    def produce(self):
        light=self._getenv("light").env
        self.energe+=light[self.rect.x][self.rect.y]*self.produce_rate
        light[self.rect.x][self.rect.y]-=self.light_waste  #光照每50tick回复一次
    def move(self,dx,dy):
        self.rect.x+=dx
        if self.rect.x<3:
            self.rect.x=3
        self.rect.y+=dy
        if self.rect.y<3:
            self.rect.y=3

        if self.rect.x>self.width-self.rect.width-3:
            self.rect.x=self.width-self.rect.width-3
        if self.rect.y>self.hight-self.rect.height-3:
            self.rect.y=self.hight-self.rect.height-3

    #调用soul的api来决定自己的行动，目前只能做到移动#TODO：增加soul的能力
    def think(self):
        light_env=self._getenv("light")
        light=light_env.get(self.rect.x,self.rect.y)
        # if light*120>100:
        #     return self.action_space[0]
        light=light_env.get_view(self.rect.center,self.view_distance)
        light=light.reshape((16))
        obs=np.array(light,dtype=np.float16)
        act=self.soul.think(obs)
        return act
        values=np.random.random(5)
        values=values+self.move_bias*6
        act=self.action_space[np.argmax(values)]
        return act

    #执行行动#TODO：改为私有函数
    def act(self):
        think=self.think()
        self.action=self.think
        if think==self.action_space[0]:
            pass
        else:
            self.energe-=1
            if think==self.action_space[1]:
                self.move(self.speed,0)
            elif think==self.action_space[2]:
                self.move(-self.speed,0)
            elif think==self.action_space[3]:
                self.move(0,self.speed)
            elif think==self.action_space[4]:
                self.move(0,-self.speed)
            else:
                print("不符合动作空间",think)

    #模拟一步，函数名是pygame的要求，根据环境、object自身状态更新object的状态（但是不直接负责移动或其他）
    def update(self, *args: any) -> None:
        self.act()
        if self.width-self.rect.x<5 or self.hight-self.rect.y<5:
            self.die()
        elif self.energe > self.born_energe:
            self.born()
        elif self.energe<self.dead_energe:
            self.die()
        if self.age>=self.max_age:
            self.die()
        self.produce()
        self.energe-=self.constant_waste
        self.age+=1
        # self.rect.x+=(random.random()-0.5)*10
        # if self.rect.x<0:
        #     self.rect.x=0
        # self.rect.y+=(random.random()-0.5)*10
        # if self.rect.y<0:
        #     self.rect.y=0

        # if self.rect.x>self.width-self.rect.width:
        #     self.rect.x=self.width-self.rect.width
        # if self.rect.y>self.hight-self.rect.height:
        #     self.rect.y=self.hight-self.rect.height
