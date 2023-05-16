from soul import SoulPool
from pygame.sprite import Sprite
from header import Rect
import numpy as np

class Object(Sprite):
    def __init__(self,rect: Rect,gene:np.int128) -> None:
        self.rect=rect
        self.gene=gene
    def _mutate(self):
        pass
    def _move(self,move_avalible:function):
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