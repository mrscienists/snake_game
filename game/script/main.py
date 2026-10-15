import pygame as p
import pygame_widgets as pw
from pygame_widgets.button import Button
from typing import Literal
import random
from snake import Snake
import settings as st

def start():
    global game_stage
    start_button.hide()
    game_stage = "game"

def fill_bg(image: p.Surface, screen: p.Surface):
    for x in range(0, st.WIDTH, 64):
        for y in range(0, st.HEIGHT, 64):
            screen.blit(image, (x, y))

# pygame setup
game_field = []
p.init()
side_width = 100
screen = p.display.set_mode((st.WIDTH + side_width, st.HEIGHT))

for _ in range(0, st.WIDTH, st.WIDTH // (st.CELL_AMOUNT * 2)):
    game_field.append(["N"] * (st.HEIGHT // st.CELL_SIZE))
snake = Snake(game_field, screen, st.CELL_SIZE)

start_btt_width = 300
start_btt_height = 150
start_button = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    (st.WIDTH - start_btt_width) // 2,  # X-coordinate of top left corner
    (st.HEIGHT - start_btt_height) // 2,  # Y-coordinate of top left corner
    start_btt_width,  # Width
    start_btt_height,  # Height

    # Optional Parameters
    text="Start game",  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=start  # Function to call when clicked on
)

#hardness = 0
#hard_mode_btt = Button(

#)

clock = p.time.Clock()
background_image = p.image.load("game/sprites/endless_bg.png").convert()

running = True
crushed = False
win = False
last_move = 0
score = 0

game_stage = "start"
while running:
    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            running = False

        if game_stage == "game":
            if event.type == p.KEYDOWN:
                match event.key:
                    case p.K_w:
                        move_to = "up"
                    case p.K_s:
                        move_to ="down"
                    case p.K_a:
                        move_to = "left"
                    case p.K_d:
                        move_to = "right"

    if game_stage == "game":
        snake.create_apple(2)

        try:
            if game_stage == 1:
                now = p.time.get_ticks()

            if now - last_move >= st.MOVE_DELAY:
                movement_result = snake.move(move_to)
                last_move = now

            match movement_result["eaten"]:
                case "red":
                    score += 1

                case "blue":
                    score += 5

                case "pink":
                    score += 10

            match movement_result["happened"]:
                case "win":
                    win = True

                case "crushed":
                    crushed = True

            movement_result = {}
        except:
            pass

    if win: game_stage = "win"
    elif crushed: game_stage = "lose"

    screen.fill("#007D06")
    fill_bg(background_image, screen)

    if game_stage == "game" :snake.draw()
    
    text_color = (255, 255, 255)

    txt_score_font_size = 36
    txt_score_font = p.font.SysFont("Arial", txt_score_font_size)
    txt_score_text_surface = txt_score_font.render(f"Score:", True, text_color)            
    screen.blit(txt_score_text_surface, 
                txt_score_text_surface.get_rect(center=(st.WIDTH + side_width // 2, 
                                                txt_score_font_size//2)))

    score_font_size = 36
    score_font = p.font.SysFont("Arial", score_font_size)
    score_text_surface = score_font.render(f"{score}", True, text_color)            
    screen.blit(score_text_surface, 
                score_text_surface.get_rect(center=(st.WIDTH + side_width // 2, 
                                              score_font_size//2 + txt_score_font_size)))

    if game_stage == 3: pass
    
    pw.update(events)
    p.display.update()
    clock.tick(240)

p.quit()