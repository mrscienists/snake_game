import pygame as p
import pygame_widgets as pw
from pygame_widgets.button import Button

class Snake:
    cordx = 5
    length = 0
    def __init__(self, field) -> None:
        sprite_pathes = {"def": "game/sprites/snake/default.png",
                         "end": "game/sprites/snake/special/end.png",
                         "head": "game/sprites/snake/special/head.png",
                         "turn": "game/sprites/snake/turn.png"}

        sprites = {}

        for sprite_path in sprite_pathes:
            sprites[sprite_path] = p.image.load(sprite_pathes[sprite_path]).convert_alpha()

        self.sprites = sprites
        
        self.cordy = len(field) // 2 - 1
        print(len(field), self.cordy)
        self.field = field
        self.field[self.cordy][self.cordx] = "HR"
        self.field[self.cordy][self.cordx - 1] = "ER"


    def draw(self):
        y = 0
        for row in self.field:
            x = 0
            for cell in row:
                #checking code on field-matrix
                #1st letter - part type (N - none (do not draw), D - default, T - turn, H - head, E - end)
                #2nt letter - in which direction part watches (R - right, L - left, U - up, D - down)
                #3rd letter (only T types) - directions that it turns (R - right, L - left, U - up, D - down)

                match cell[0]:
                    case "D":
                        match cell[1]:
                            case "R": 
                                screen.blit(self.sprites["def"], (x, y))
                            case "L":
                                screen.blit(self.sprites["def"], (x, y))

                            case "U":
                                screen.blit(p.transform.rotate(self.sprites["def"], 90), (x, y))
                            case "D":
                                screen.blit(p.transform.rotate(self.sprites["def"], 90), (x, y))

                    case "T":
                        match cell[1]:
                            case "R":

                                match cell[2]:
                                    case "U":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 270), (x, y))
                                    case "D":
                                        screen.blit(self.sprites["turn"], (x, y))

                            case "L":
                                match cell[2]:
                                    case "U":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 180), (x, y))
                                    case "D":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 90), (x, y))

                            
                            case "U":
                                match cell[2]:
                                    case "R":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 90), (x, y))
                                    case "L":
                                        screen.blit(self.sprites["turn"], (x, y))

                            
                            case "D":
                                match cell[2]:
                                    case "R":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 180), (x, y))
                                    case "L":
                                        screen.blit(p.transform.rotate(self.sprites["turn"], 270), (x, y))

                    case "H":
                        match cell[1]:
                            case "R":
                                screen.blit(self.sprites["head"], (x, y))
                            case "D":
                                screen.blit(p.transform.rotate(self.sprites["head"], 90), (x, y))
                            case "L":
                                screen.blit(p.transform.rotate(self.sprites["head"], 180), (x, y))
                            case "D":
                                screen.blit(p.transform.rotate(self.sprites["head"], 270), (x, y))

                    case "E":
                        match cell[1]:
                            case "R":
                                screen.blit(self.sprites["end"], (x, y))
                            case "D":
                                screen.blit(p.transform.rotate(self.sprites["end"], 90), (x, y))
                            case "L":
                                screen.blit(p.transform.rotate(self.sprites["end"], 180), (x, y))
                            case "D":
                                screen.blit(p.transform.rotate(self.sprites["end"], 270), (x, y))

                x += 32
            y += 32

    def move(self, direction: str):
        for row in self.field:
            print(row)

        match direction:
            case "right":
                self.__go_right__()

    def __go_right__(self):
        pass

def start():
    global screen, button, level
    strt_button.hide()
    level += 1

def fill_bg(img: p.Surface):
    for x in range(0, WIDTH, 64):
        for y in range(0, HEIGHT, 64):
            screen.blit(img, (x, y))

# pygame setup
CELL_AMOUNT = 10
WIDTH, HEIGHT = 64 * CELL_AMOUNT, 64 * CELL_AMOUNT

field = []
for columns in range(0, WIDTH, WIDTH // (CELL_AMOUNT * 2)):
    field.append(["N"] * (HEIGHT // 32))
p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
snake = Snake(field)

clock = p.time.Clock()
level = 0
bg = p.image.load("game/sprites/endless_bg.png").convert()
btt_width = 300
btt_height = 150

strt_button = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    (WIDTH - btt_width)//2,  # X-coordinate of top left corner
    (HEIGHT - btt_height)//2,  # Y-coordinate of top left corner
    btt_width,  # Width
    btt_height,  # Height

    # Optional Parameters
    text='Hello',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=start  # Function to call when clicked on
)

running = True
while running:
    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            running = False
        
        if level == 1:
            if event.type == p.KEYDOWN :
                match event.key:
                    case p.K_w:
                        print("w")
                    case p.K_s:
                        print("s")
                    case p.K_a:
                        print("a")
                    case p.K_d:
                        snake.move("right")
 
    fill_bg(bg)
    snake.draw()
    pw.update(events)  # Call once every loop to allow widgets to render and listen
    p.display.update()
    p.display.flip()
    clock.tick(60)
        
p.quit()