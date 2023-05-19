import pygame
import threading
import time
import random
import numpy as np
from soul import Soul
from env import Light,Positon
from Object import V
HIGHT=600
WIDTH=600


VDIE=2555
LIGHTUPDATA=2556



agent_sprite=pygame.sprite.Group()
clock=pygame.time.Clock()
light=Light("light",WIDTH,HIGHT)
space=Positon("space",WIDTH,HIGHT)
env={light.name:light,space.name:space}
def main():
    win=pygame.display.set_mode((WIDTH,HIGHT))
    pygame.display.set_caption("模拟文明")
    win.fill((255,255,255))
    pygame.display.update()
    #pygame.time.set_timer(LIGHTUPDATA,5000)
    for i in range(1000):
        agent_sprite.add(V(Soul(range(16),range(5),None),env,random.randint(0,WIDTH-12)+5,random.randint(0,HIGHT-12)+5))
        #agent_sprite.add(V(Soul(range(16),range(5),None),env,WIDTH//2,HIGHT//2))
    groups=[agent_sprite]
    while True:
        clock.tick(144)
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
        current=pygame.sprite.GroupSingle()
        for i in groups[0]:
            current.add(i)
            c=pygame.sprite.groupcollide(current,groups[0],False,False)
            if len(c)>1:
                i.kill()
        for group in groups:
            group.update()
            group.draw(win)
        if clock.get_time()%50==0:
            print("更新光照")
            light.update()
        pygame.display.update()
        print(clock.get_fps(),"nums",len(groups[0]))
        if len(groups[0])<=0:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        


main()
