import pygame as p
import pygame_widgets as pw
from pygame_widgets.button import Button

CELL_SIZE = 32

class Snake:
    DIRECTION_OFFSETS = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    head_x = 5
    length = 1

    def __init__(self, game_field, screen) -> None:
        sprite_paths = {"def": "game/sprites/snake/default.png",
                        "end": "game/sprites/snake/special/end.png",
                        "head": "game/sprites/snake/special/head.png",
                        "t_end_l": "game/sprites/snake/special/turn_end/turn_end_left.png",
                        "t_end_r": "game/sprites/snake/special/turn_end/turn_end_right.png",
                        "turn": "game/sprites/snake/turn.png",
                        "r_apple": "game/sprites/apples/apple_red.png",
                        "b_apple": "game/sprites/apples/apple_blue.png",
                        "p_apple": "game/sprites/apples/apple_pink.png"}

        loaded_sprites = {}

        for sprite_name in sprite_paths:
            loaded_sprites[sprite_name] = p.image.load(sprite_paths[sprite_name]).convert_alpha()

        self.sprites = loaded_sprites
        self.screen = screen
        self.head_y = len(game_field) // 2 - 1
        print(len(game_field), self.head_y)
        self.field = game_field

        self.field[self.head_y][self.head_x] = "HU"
        self.field[self.head_y + 1][self.head_x] = "DU"
        self.field[self.head_y + 2][self.head_x] = "EU"
        self.field[10][10] = "A"

    def draw(self):
        pixel_y = 0
        for row_cells in self.field:
            pixel_x = 0
            for cell_code in row_cells:
                # checking code on field-matrix
                # 1st letter - part type (N - none (do not draw), D - default, T - turn, H - head, E - end)
                # 2nd letter - in which direction part watches (R - right, L - left, U - up, D - down)
                # 3rd letter (Except D types) - directions that it turns (R - right, L - left, U - up, D - down)

                part_type = cell_code[0]
                facing = cell_code[1] if len(cell_code) > 1 else None
                turn_to = cell_code[2] if len(cell_code) > 2 else None
                position = (pixel_x, pixel_y)

                match part_type:
                    case "D":
                        match facing:
                            case "R":
                                self.screen.blit(self.sprites["def"], position)
                            case "L":
                                self.screen.blit(self.sprites["def"], position)

                            case "U":
                                self.screen.blit(p.transform.rotate(self.sprites["def"], 90), position)
                            case "D":
                                self.screen.blit(p.transform.rotate(self.sprites["def"], 90), position)

                    case "T":
                        match facing:
                            case "R":
                                match turn_to:
                                    case "U":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 270), position)
                                    case "D":
                                        self.screen.blit(self.sprites["turn"], position)

                            case "L":
                                match turn_to:
                                    case "U":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 180), position)
                                    case "D":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 90), position)

                            case "U":
                                match turn_to:
                                    case "R":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 90), position)
                                    case "L":
                                        self.screen.blit(self.sprites["turn"], position)

                            case "D":
                                match turn_to:
                                    case "R":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 180), position)
                                    case "L":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 270), position)

                    case "H":
                        if len(cell_code) == 2:
                            match facing:
                                case "R":
                                    self.screen.blit(self.sprites["head"], position)
                                case "D":
                                    self.screen.blit(p.transform.rotate(self.sprites["head"], 270), position)
                                case "L":
                                    self.screen.blit(p.transform.rotate(self.sprites["head"], 180), position)
                                case "U":
                                    self.screen.blit(p.transform.rotate(self.sprites["head"], 90), position)
                        else:
                            match facing:
                                case "R":
                                    match turn_to:
                                        case "U":
                                            self.screen.blit(self.sprites["t_head_l"], position)
                                        case "D":
                                            self.screen.blit(self.sprites["t_head_r"], position)

                                case "D":
                                    match turn_to:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_r"], 270), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_l"], 270), position)

                                case "L":
                                    match turn_to:
                                        case "U":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_r"], 180), position)
                                        case "D":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_l"], 180), position)

                                case "U":
                                    match turn_to:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_l"], 90), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_head_r"], 90), position)

                    case "E":
                        if len(cell_code) == 2:
                            match facing:
                                case "R":
                                    self.screen.blit(self.sprites["end"], position)
                                case "D":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 270), position)
                                case "L":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 180), position)
                                case "U":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 90), position)
                        else:
                            match facing:
                                case "R":
                                    match turn_to:
                                        case "U":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 180), position)
                                        case "D":
                                            self.screen.blit(self.sprites["t_end_r"], position)

                                case "D":
                                    match turn_to:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 270), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 90), position)

                                case "L":
                                    match turn_to:
                                        case "U":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 180), position)
                                        case "D":
                                            self.screen.blit(self.sprites["t_end_l"], position)

                                case "U":
                                    match turn_to:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 270), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 90), position)
                
                    case "A":
                        self.screen.blit(self.sprites["r_apple"], position)

                pixel_x += CELL_SIZE
            pixel_y += CELL_SIZE

    def move(self, direction: str):
        match direction:
            case "right":
                self.__go_right__()
            case "up":
                self.__go_up__()
            case "left":
                self.__go_left__()
            case "down":
                self.__go_down__()

    def __go_right__(self) -> bool:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "L":
                        return False

                    if x + 1 >= len(self.field[0]):
                        return True
                    elif self.field[y][x + 1] != "N" and \
                            self.field[y][x + 1][0] != "A":
                        return True

                    grow = self.field[y][x + 1][0] == "A"

                    if facing != "R":
                        self.field[y][x] = f"T{facing}R"
                    else:
                        self.field[y][x] = "DR"
                    self.field[y][x + 1] = "HR"

                    if grow:
                        self.length += 1
                        break

                    match facing:
                        case "R":
                            x -= 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "D" | "T":
                    match self.field[y][x][1]:
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "E":
                    step_y, step_x = self.DIRECTION_OFFSETS[self.field[y][x][-1]]
                    next_y, next_x = y + step_y, x + step_x

                    self.field[y][x] = "N"
                    self.field[next_y][next_x] = "E" + self.field[next_y][next_x][1:]
                    break

        self.head_x += 1
        return False

    def __go_up__(self) -> bool:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "D":                    # на 180° разворачиваться нельзя
                        return False

                    if y - 1 < 0:                        # crushed into wall
                        return True
                    elif self.field[y - 1][x] != "N" and \
                            self.field[y - 1][x][0] != "A":   # crushed into itself
                        return True

                    grow = self.field[y - 1][x][0] == "A"

                    if facing != "U":                    # e.c.: HR -> "TRU"
                        self.field[y][x] = f"T{facing}U"
                    else:
                        self.field[y][x] = "DU"
                    self.field[y - 1][x] = "HU"          # новая голова

                    if grow:
                        self.length += 1
                        break

                    match facing:                        # шаг назад по телу
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "U":
                            y += 1

                case "D" | "T":
                    match self.field[y][x][1]:
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "E":
                    step_y, step_x = self.DIRECTION_OFFSETS[self.field[y][x][-1]]
                    next_y, next_x = y + step_y, x + step_x

                    self.field[y][x] = "N"
                    self.field[next_y][next_x] = "E" + self.field[next_y][next_x][1:]
                    break

        self.head_y -= 1
        return False

    def __go_left__(self) -> bool:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "R":
                        return False

                    if x - 1 < 0:
                        return True
                    elif self.field[y][x - 1] != "N" and \
                            self.field[y][x - 1][0] != "A":
                        return True

                    grow = self.field[y][x - 1][0] == "A"

                    if facing != "L":
                        self.field[y][x] = f"T{facing}L"
                    else:
                        self.field[y][x] = "DL"
                    self.field[y][x - 1] = "HL"

                    if grow:
                        self.length += 1
                        break

                    match facing:
                        case "L":
                            x += 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "D" | "T":
                    match self.field[y][x][1]:
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "E":
                    step_y, step_x = self.DIRECTION_OFFSETS[self.field[y][x][-1]]
                    next_y, next_x = y + step_y, x + step_x

                    self.field[y][x] = "N"
                    self.field[next_y][next_x] = "E" + self.field[next_y][next_x][1:]
                    break

        self.head_x -= 1
        return False

    def __go_down__(self) -> bool:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "U":
                        return False

                    if y + 1 >= len(self.field):
                        return True
                    elif self.field[y + 1][x] != "N" and \
                            self.field[y + 1][x][0] != "A":
                        return True

                    grow = self.field[y + 1][x][0] == "A"

                    if facing != "D":
                        self.field[y][x] = f"T{facing}D"
                    else:
                        self.field[y][x] = "DD"
                    self.field[y + 1][x] = "HD"

                    if grow:
                        self.length += 1
                        break

                    match facing:
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "D":
                            y -= 1

                case "D" | "T":
                    match self.field[y][x][1]:
                        case "R":
                            x -= 1
                        case "L":
                            x += 1
                        case "U":
                            y += 1
                        case "D":
                            y -= 1

                case "E":
                    step_y, step_x = self.DIRECTION_OFFSETS[self.field[y][x][-1]]
                    next_y, next_x = y + step_y, x + step_x

                    self.field[y][x] = "N"
                    self.field[next_y][next_x] = "E" + self.field[next_y][next_x][1:]
                    break

        self.head_y += 1
        return False

def start():
    global game_stage
    start_button.hide()
    game_stage += 1

def fill_bg(image: p.Surface, screen: p.Surface):
    for x in range(0, WIDTH, 64):
        for y in range(0, HEIGHT, 64):
            screen.blit(image, (x, y))


# pygame setup
CELL_AMOUNT = 10
WIDTH, HEIGHT = 64 * CELL_AMOUNT, 64 * CELL_AMOUNT

game_field = []
for _ in range(0, WIDTH, WIDTH // (CELL_AMOUNT * 2)):
    game_field.append(["N"] * (HEIGHT // CELL_SIZE))
p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
snake = Snake(game_field, screen)

clock = p.time.Clock()
game_stage = 0
background_image = p.image.load("game/sprites/endless_bg.png").convert()
button_width = 300
button_height = 150

start_button = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    (WIDTH - button_width) // 2,  # X-coordinate of top left corner
    (HEIGHT - button_height) // 2,  # Y-coordinate of top left corner
    button_width,  # Width
    button_height,  # Height

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

        if game_stage == 1:
            if event.type == p.KEYDOWN:
                match event.key:
                    case p.K_w:
                        snake.move("up")
                    case p.K_s:
                        snake.move("down")
                    case p.K_a:
                        snake.move("left")
                    case p.K_d:
                        snake.move("right")

    fill_bg(background_image, screen)
    snake.draw()
    pw.update(events)
    p.display.update()
    clock.tick(60)

p.quit()