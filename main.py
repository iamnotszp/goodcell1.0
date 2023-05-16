import pygame
import threading
import time
import random
import numpy as np
from soul import Soul
HIGHT=600
WIDTH=1200

class Mana:
    def __init__(self,name:str,*args,**kwargs):
        pass
    def update(self):
        pass
    def get(self):
        raise Exception("不允许不定义使用Mana.get")

class Positon(Mana):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
    def get(x,y):
        return (x,y)

class Light(Mana):
    def __init__(self, name: str, *args, **kwargs):
        self.name=name
        self.env=np.random.random((WIDTH,HIGHT))
        self.bias=np.zeros((WIDTH,HIGHT))
        for i in range(100,300):
            self.bias[i][100:300]+=self.env[i][100:300]
        self.env=np.random.random((WIDTH,HIGHT))+self.bias*0.7
        self.glass=np.zeros((WIDTH,HIGHT))
        for i in range(WIDTH):
            for j in range(HIGHT):
                self.glass[i][j]=(i/2+j)*1.3/(WIDTH+HIGHT)
        self.update()
    def update(self):
        print("light has updated")
        self.env=np.random.random((WIDTH,HIGHT))*0.25+self.bias*0.5+self.glass*0.9
        #self.env=(np.tanh(self.env)+1)/2
        #self.env=np.tanh(np.random.random((WIDTH,HIGHT))+1)/2
    def get(self,x,y):
        return self.env[x][y]
    def get_view(self,xy:tuple,size)->np.ndarray:
        x=xy[0]
        y=xy[1]
        view= self.env[x-size:x+size,y-size:y+size]
        return view
    def get_all(self)->np.ndarray:
        return self.env

VDIE=2555
LIGHTUPDATA=2556

class V(pygame.sprite.Sprite):
    i=1
    @staticmethod
    def _getid():
        V.i=V.i+1
        return V.i


    def __init__(self,x=0,y=0,speed=3,face="D:\my神经网络\pygame\居民.jpg", env={"position":Positon("default")},move_bias=np.zeros(5)) -> None:
        super().__init__()
        #self.image=pygame.image.load(face)
        self.rect=pygame.rect.Rect(x,y,2,2)
        self.image=pygame.surfarray.make_surface(np.ones((self.rect.w,self.rect.h,3))*255)
        self.action_space=range(5)
        self.observe_space=range(9)
        self.action=0
        self.speed=speed
        if not env.get("position"):
            env["position"]=Positon("default")
        self.env=env
        self.energe=3000
        self.id=self._getid()
        self.move_bias=move_bias
        self.age=0
        self.soul=Soul(self.observe_space,self.action_space)
    
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
            i.add(V(random.randint(0,WIDTH-1),random.randint(0,HIGHT-1),env=self.env, move_bias = self.move_bias+np.random.random(len(self.action_space))*0.1))

    def produce(self):
        light=self._getenv("light").env
        self.energe+=light[self.rect.x][self.rect.y]*120
    def move(self,dx,dy):
        self.rect.x+=dx
        if self.rect.x<0:
            self.rect.x=0
        self.rect.y+=dy
        if self.rect.y<0:
            self.rect.y=0

        if self.rect.x>WIDTH-self.rect.width:
            self.rect.x=WIDTH-self.rect.width
        if self.rect.y>HIGHT-self.rect.height:
            self.rect.y=HIGHT-self.rect.height

    def think(self):
        light_env=self._getenv("light")
        light=light_env.get(self.rect.x,self.rect.y)
        if light*120>100:
            return self.action_space[0]
        light=light_env.get_view(self.rect.center,1)
        light.reshape((9))
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
                self.move(3,0)
            elif think==self.action_space[2]:
                self.move(-3,0)
            elif think==self.action_space[3]:
                self.move(0,3)
            elif think==self.action_space[4]:
                self.move(0,-3)
            else:
                print("不符合动作空间",think)

    def update(self, *args: any) -> None:
        self.act()
        if self.energe > 6000:
            self.born()
        elif self.energe<500:
            self.die()
        if self.age>=5000:
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

        # if self.rect.x>WIDTH-self.rect.width:
        #     self.rect.x=WIDTH-self.rect.width
        # if self.rect.y>HIGHT-self.rect.height:
        #     self.rect.y=HIGHT-self.rect.height


agent_sprite=pygame.sprite.Group()
clock=pygame.time.Clock()
light=Light("light")
def main():
    win=pygame.display.set_mode((WIDTH,HIGHT))
    pygame.display.set_caption("模拟文明")
    win.fill((255,255,255))
    pygame.display.update()
    pygame.time.set_timer(LIGHTUPDATA,1000)
    for i in range(5000):
        agent_sprite.add(V(random.randint(0,WIDTH-1),random.randint(0,HIGHT-1),env={light.name:light}))
    groups=[agent_sprite]
    while True:
        clock.tick(20)
        event=pygame.event.get()
        for e in event:
            #print(e.type)
            if e.type==pygame.QUIT:
                pygame.quit()
                exit()
            if e.type==VDIE:
                spirit=e.V
                print(spirit)
                spirit.kill()
            if e.type==LIGHTUPDATA:
                light.update()
                
        #collision=pygame.sprite.groupcollide(agent_sprite,agent_sprite,True,True)
        #agent_sprite.add(V(random.randint(0,WIDTH),random.randint(0,HIGHT),env={light.name:light}))

        # win.fill((255,255,255))
        win.blit(pygame.surfarray.make_surface(light.get_all()),(0,0))
        for group in groups:
            group.update()
            group.draw(win)
        # if clock.get_time()%5==0:
        #     print("更新光照")
        #     light.update()
        pygame.display.update()
        print(clock.get_fps(),"nums",len(groups[0]))
        if len(groups[0])<=0:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        


main()
