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
    @staticmethod
    def _getid():
        V.i=V.i+1
        return V.i


    def __init__(self,soul:Soul,env,x=0,y=0,speed=3,face="D:\my神经网络\pygame\居民.jpg",move_bias=np.zeros(5)) -> None:
        super().__init__()
        #self.image=pygame.image.load(face)
        self.rect=pygame.rect.Rect(x,y,2,2)
        self.image=pygame.surfarray.make_surface(np.ones((self.rect.w,self.rect.h,3))*255)
        self.action_space=range(5)
        self.observe_space=range(16)
        self.action=0
        self.speed=speed
        self.born_energe=6000
        self.max_age=15000
        self.view_distance=2
        if not env.get("space"):
            raise Exception("错误，未设置space环境")
        self.env=env
        self.width,self.hight=self._getenv("space").get_w_d()
        self.energe=3000
        self.id=self._getid()
        self.move_bias=move_bias
        self.age=0
        self.soul=soul
    
    def _getenv_all(self):
        result=[]
        for key,val in self.env:
            result.append((key,val))
        return result

    def _getenv(self,name:str):
        return self.env.get(name)

    def die(self):
        #print(self.id,"is dying")
        if random.random()<0.05:
            print(self.id,"died")
            self.kill()
    
    def born(self):
        if self.energe<=3000:
            return
        for i in self.groups():
            self.energe-=3000
            i.add(V(self.soul,self.env,random.randint(0,self.width-12)+5,random.randint(0,self.hight-12)+5, move_bias = self.move_bias+np.random.random(len(self.action_space))*0.1))

    def produce(self):
        light=self._getenv("light").env
        self.energe+=light[self.rect.x][self.rect.y]*240
        light[self.rect.x][self.rect.y]-=0.01  #光照每50tick回复一次
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

    def update(self, *args: any) -> None:
        self.act()
        if self.width-self.rect.x<5 or self.hight-self.rect.y<5:
            self.die()
        elif self.energe > self.born_energe:
            self.born()
        elif self.energe<500:
            self.die()
        if self.age>=self.max_age:
            self.die()
        self.produce()
        self.energe-=100
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
