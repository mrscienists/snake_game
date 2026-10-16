import pygame as p
import pygame_widgets as pw
from pygame_widgets.button import Button
from typing import Literal
import random
from snake import Snake
import settings as st

def reset_values():
    global snake, move_to, movement_result, score, running, crushed, win, last_move, game_field

    try: del snake
    except: pass

    try: del game_field
    except: pass

    try: del move_to
    except: pass

    try: del movement_result
    except: pass

    score = 0
    running = True
    crushed = False
    win = False
    last_move = 0

def start():
    global game_stage, snake
    start_button.hide()
    restart_button.hide()
    game_stage = "game"

    game_field = []
    for _ in range(0, st.WIDTH, st.WIDTH // (st.CELL_AMOUNT * 2)):
        game_field.append(["N"] * (st.HEIGHT // st.CELL_SIZE))

    reset_values()

    snake = Snake(game_field, screen, st.CELL_SIZE)

def restart():
    global game_stage
    game_stage = "start"
    restart_button.hide()
    exit_button.hide()

def fill_bg(image: p.Surface, screen: p.Surface):
    for x in range(0, st.WIDTH, 64):
        for y in range(0, st.HEIGHT, 64):
            screen.blit(image, (x, y))

def break_loop():
    global running
    running = False

def change_difficult(difficult: Literal["easy", "medium", "hard"]):
    global difficulty_speed_coeff, difficulty_score_coeff

    match difficult:
        case "easy":
            difficulty_speed_coeff = st.EASY_MODE_SPEED_MULT
            difficulty_score_coeff = st.EASY_MODE_SCORE_MULT
        case "medium":
            difficulty_speed_coeff = st.MEDIUM_MODE_SPEED_MULT
            difficulty_score_coeff = st.MEDIUM_MODE_SCORE_MULT
        case "hard":
            difficulty_speed_coeff = st.HARD_MODE_SPEED_MULT
            difficulty_score_coeff = st.HARD_MODE_SCORE_MULT
        case _:
            pass

def make_difficulty_button(text: str, difficult: Literal["easy", "medium", "hard"],
                           inactive: str, hover: str, pressed: str) -> Button:
    button = Button(
        screen,
        0, 0,  # позиция выставляется в главном цикле
        hardness_btt_width,
        hardness_btt_height,

        text=text,
        fontSize=hardness_font_size,
        fontColour="#CACACA",
        margin=20,
        inactiveColour=inactive,
        hoverColour=hover,
        pressedColour=pressed,
        radius=20,
        onClick=lambda: change_difficult(difficult)
    )
    button.hide()
    return button

# pygame setup
p.init()
side_width = 100
screen = p.display.set_mode((st.WIDTH + side_width, st.HEIGHT))

btt_width = 170
btt_height = 40
btt_font_size = 30
btt_inactive_colour="#FEA750" #Default btt color
btt_hover_colour="#FF8000" #When cursor moved to btt
btt_pressed_color="#FFBB00" #When btt is pressed
start_button = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    (st.WIDTH - btt_width) // 2,  # X-coordinate of top left corner
    (st.HEIGHT - btt_height) // 2,  # Y-coordinate of top left corner
    btt_width,  # Width
    btt_height,  # Height

    # Optional Parameters
    text="Start game",  # Text to display
    fontSize=btt_font_size,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=btt_inactive_colour,  # Colour of button when not being interacted with
    hoverColour=btt_hover_colour,  # Colour of button when being hovered over
    pressedColour=btt_pressed_color,  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=start  # Function to call when clicked on
)
start_button.hide()

restart_button = Button(
            # Mandatory Parameters
            screen,  # Surface to place button on
            (st.WIDTH - btt_width) // 2,  # X-coordinate of top left corner
            (st.HEIGHT - btt_height) // 2,  # Y-coordinate of top left corner
            btt_width,  # Width
            btt_height,  # Height

            # Optional Parameters
            text="Restart game",  # Text to display
            fontSize=btt_font_size,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=btt_inactive_colour,  # Colour of button when not being interacted with
            hoverColour=btt_hover_colour,  # Colour of button when being hovered over
            pressedColour=btt_pressed_color,  # Colour of button when being clicked
            radius=20,  # Radius of border corners (leave empty for not curved)
            onClick=restart # Function to call when clicked on
        )
restart_button.hide()

exit_button = Button(
    screen,
    (st.WIDTH - btt_width) // 2,  # X-coordinate of top left corner
    (st.HEIGHT - btt_height) // 2,  # Y-coordinate of top left corner
    btt_width,  # Width
    btt_height,  # Height

    # Optional Parameters
    text="Exit",  # Text to display
    fontSize=btt_font_size,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=btt_inactive_colour,  # Colour of button when not being interacted with
    hoverColour=btt_hover_colour,  # Colour of button when being hovered over
    pressedColour=btt_pressed_color,  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=break_loop # Function to call when clicked on
)
exit_button.hide()

hardness_btt_width = 200
hardness_btt_height = 40
hardness_font_size = 30
gap_between_btt = 10
easy_btt = make_difficulty_button("Easy mode", "easy",
                                  "#2FBF3B", "#1E8C28", "#14661C")
medium_btt = make_difficulty_button("Medium mode", "medium",
                                    "#E6A800", "#B38300", "#805D00")
hard_btt = make_difficulty_button("Hard mode", "hard",
                                  "#FD2828", "#A90000", "#7F0000")

difficulty_buttons = [easy_btt, medium_btt, hard_btt]
clock = p.time.Clock()

running = True
crushed = False
win = False
last_move = 0
score = 0
difficulty_speed_coeff = st.EASY_MODE_SPEED_MULT
game_stage = "start"
while running:
    screen.fill("#007D06")
    fill_bg(p.image.load("game/sprites/endless_bg.png").convert(), screen)

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

    text_color = "#FFFFFF"

    if game_stage == "start":
        name_size = 50
        placement_of_name = (st.WIDTH // 2, 
                             (st.HEIGHT - name_size) // 2)

        name_font = p.font.SysFont("Arial", name_size)
        name_text_surface = name_font.render(f"Snake & apple!", True, text_color)
        screen.blit(name_text_surface,
        name_text_surface.get_rect(center=placement_of_name))

        start_button.show()
        start_button._x = placement_of_name[0] - btt_width // 2
        start_button._y = placement_of_name[1] + btt_height

        for i, button in enumerate(difficulty_buttons, start=1):
            button.show()
            button._x = (st.WIDTH - hardness_btt_width) // 2
            button._y = start_button._y + (btt_height + gap_between_btt) * i

    elif game_stage == "game":
        snake.create_apple(400)
        try:
            if game_stage == "game":
                now = p.time.get_ticks()

            if now - last_move >= st.MOVE_DELAY * difficulty_speed_coeff:
                movement_result = snake.move(move_to)
                last_move = now

            match movement_result["eaten"]:
                case "red":
                    score += 1 * difficulty_score_coeff

                case "blue":
                    score += 5 * difficulty_score_coeff

                case "pink":
                    score += 10 * difficulty_score_coeff

            match movement_result["happened"]:
                case "win":
                    score += 100 * difficulty_score_coeff
                    win = True

                case "crushed":
                    crushed = True

            movement_result = {}
        except:
            pass

        snake.draw()

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
        
        if win: game_stage = "win"
        elif crushed: game_stage = "lose"

    elif game_stage == "win":
        restart_button.show()

        win_font_size = 50
        sub_win_font_size = 36
        placement_of_win = (st.WIDTH // 2,
                            (st.HEIGHT - win_font_size - sub_win_font_size * 2) // 2)

        win_font = p.font.SysFont("Arial", win_font_size)
        win_text_surface = win_font.render(f"YOU WON!", True, text_color)
        screen.blit(win_text_surface,
        win_text_surface.get_rect(center=placement_of_win))

        txt_score_font = p.font.SysFont("Arial", sub_win_font_size)
        txt_score_text_surface = txt_score_font.render(f"Score:", True, text_color)
        screen.blit(txt_score_text_surface, 
                    txt_score_text_surface.get_rect(center=(placement_of_win[0], placement_of_win[1] + sub_win_font_size)))

        score_font = p.font.SysFont("Arial", sub_win_font_size)
        score_text_surface = score_font.render(f"{score}", True, text_color)
        screen.blit(score_text_surface,
                    score_text_surface.get_rect(center=(placement_of_win[0], placement_of_win[1] + sub_win_font_size * 2)))

        #restart btt
        restart_button.show()
        buttons_x = placement_of_win[0] - btt_width // 2
        buttons_y = placement_of_win[1] + sub_win_font_size * 3
        gap_between_btt = 10

        restart_button._x = buttons_x
        restart_button._y = buttons_y

        #exit btt
        exit_button.show()

        exit_button._x = buttons_x
        exit_button._y = buttons_y + btt_height + gap_between_btt

    elif game_stage == "lose":
        #lose text
        lose_font_size = 50
        sub_lose_font_size = 36
        placement_of_lose = (st.WIDTH // 2, 
                             (st.HEIGHT - lose_font_size - sub_lose_font_size * 2) // 2)

        lose_font = p.font.SysFont("Arial", lose_font_size)
        lose_text_surface = lose_font.render(f"YOU LOSE!", True, text_color)
        screen.blit(lose_text_surface,
        lose_text_surface.get_rect(center=placement_of_lose))

        #score text
        txt_score_font = p.font.SysFont("Arial", sub_lose_font_size)
        txt_score_text_surface = txt_score_font.render(f"Score:", True, text_color)
        screen.blit(txt_score_text_surface, 
                    txt_score_text_surface.get_rect(center=(placement_of_lose[0], placement_of_lose[1] + sub_lose_font_size)))

        score_font = p.font.SysFont("Arial", sub_lose_font_size)
        score_text_surface = score_font.render(f"{score}", True, text_color)
        screen.blit(score_text_surface,
                    score_text_surface.get_rect(center=(placement_of_lose[0], placement_of_lose[1] + sub_lose_font_size * 2)))

        #restart btt
        restart_button.show()
        buttons_x = placement_of_lose[0] - btt_width // 2
        buttons_y = placement_of_lose[1] + sub_lose_font_size * 3
        gap_between_btt = 10

        restart_button._x = buttons_x
        restart_button._y = buttons_y

        #exit btt
        exit_button.show()

        exit_button._x = buttons_x
        exit_button._y = buttons_y + btt_height + gap_between_btt

    if game_stage != "start":
        for button in difficulty_buttons:
            button.hide()

    elif game_stage == "win" or game_stage == "lose":
        pass #write_data(nickname, score)

    pw.update(events)
    p.display.update()

p.quit()