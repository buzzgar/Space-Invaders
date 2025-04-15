import stddraw 
from picture import Picture 
import GameSettings 

class Background:
  def __init__(self):
    self.background = Picture(GameSettings.background_sprite_path)
    self.w = self.background.width()
    self.h = self.background.height() 

def display(self): 
  stddraw.picture(self.background, self.w / 2, self.h / 2) 
