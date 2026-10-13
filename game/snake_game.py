import pygame as p
import pygame_widgets as pw
from pygame_widgets.button import Button

# pygame setup
p.init()
screen = p.display.set_mode((1280, 720))
clock = p.time.Clock()
running = True

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False   

p.quit()