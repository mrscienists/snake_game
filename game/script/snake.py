import pygame as p
from typing import Literal
import random

class Snake:
    DIRECTION_OFFSETS = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    head_x = 3
    length = 1
    direction = "right"
    OPPOSITE_DIRECTION = {"left":"right", 
                          "right": "left",
                          "up": "down", 
                          "down": "up"}
    
    def __init__(self, game_field, screen, cell_size) -> None:
        self.cell_size = cell_size
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
        self.field = game_field

        self.field[self.head_y][self.head_x] = "HR"
        self.field[self.head_y][self.head_x - 1] = "DR"
        self.field[self.head_y][self.head_x - 2] = "ER"
        self.field[len(self.field)//2 - 1][len(self.field[0])//2 - 1] = "AR"

    def draw(self):
        """Drawing method. Draws snake and apples"""
        pixel_y = 0
        for row_cells in self.field:
            pixel_x = 0
            for cell_code in row_cells:
                # checking code on field-matrix
                # 1st letter - part type (N - none (do not draw), D - default, T - turn, H - head, E - end)
                # 2nd letter - in which direction part watches (R - right, L - left, U - up, D - down)
                # 3rd letter (Except D types) - directions that it turns (R - right, L - left, U - up, D - down)
                position = (pixel_x, pixel_y)

                match cell_code[0]:
                    case "D":
                        match cell_code[1]:
                            case "R":
                                self.screen.blit(self.sprites["def"], position)
                            case "L":
                                self.screen.blit(self.sprites["def"], position)

                            case "U":
                                self.screen.blit(p.transform.rotate(self.sprites["def"], 90), position)
                            case "D":
                                self.screen.blit(p.transform.rotate(self.sprites["def"], 90), position)

                    case "T":
                        match cell_code[1]:
                            case "R":
                                match cell_code[2]:
                                    case "U":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 270), position)
                                    case "D":
                                        self.screen.blit(self.sprites["turn"], position)

                            case "L":
                                match cell_code[2]:
                                    case "U":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 180), position)
                                    case "D":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 90), position)

                            case "U":
                                match cell_code[2]:
                                    case "R":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 90), position)
                                    case "L":
                                        self.screen.blit(self.sprites["turn"], position)

                            case "D":
                                match cell_code[2]:
                                    case "R":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 180), position)
                                    case "L":
                                        self.screen.blit(p.transform.rotate(self.sprites["turn"], 270), position)

                    case "H":
                        match cell_code[1]:
                            case "R":
                                self.screen.blit(self.sprites["head"], position)
                            case "D":
                                self.screen.blit(p.transform.rotate(self.sprites["head"], 270), position)
                            case "L":
                                self.screen.blit(p.transform.rotate(self.sprites["head"], 180), position)
                            case "U":
                                self.screen.blit(p.transform.rotate(self.sprites["head"], 90), position)

                    case "E":
                        if len(cell_code) == 2:
                            match cell_code[1]:
                                case "R":
                                    self.screen.blit(self.sprites["end"], position)
                                case "D":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 270), position)
                                case "L":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 180), position)
                                case "U":
                                    self.screen.blit(p.transform.rotate(self.sprites["end"], 90), position)
                        else:
                            match cell_code[1]:
                                case "R":
                                    match cell_code[2]:
                                        case "U":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 180), position)
                                        case "D":
                                            self.screen.blit(self.sprites["t_end_r"], position)

                                case "D":
                                    match cell_code[2]:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 270), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 90), position)

                                case "L":
                                    match cell_code[2]:
                                        case "U":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 180), position)
                                        case "D":
                                            self.screen.blit(self.sprites["t_end_l"], position)

                                case "U":
                                    match cell_code[2]:
                                        case "L":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_l"], 270), position)
                                        case "R":
                                            self.screen.blit(p.transform.rotate(self.sprites["t_end_r"], 90), position)
                
                    case "A":
                        match cell_code[1]:
                            case "R":
                                self.screen.blit(self.sprites["r_apple"], position)
                            case "B":
                                self.screen.blit(self.sprites["b_apple"], position)
                            case "P":
                                self.screen.blit(self.sprites["p_apple"], position)

                pixel_x += self.cell_size
            pixel_y += self.cell_size

    def move(self, direction: Literal["right", "left", "up", "down"]) -> \
                dict[
                    Literal["happened", "eaten"],
                    Literal["nothing", "crushed", "win", "none", "red", "blue", "pink"]
                ]:
        
        """Snake's movement method. Returns "crished", when crushed; 
           "win", when snake fills every single cell 
           or "nothing", when nothing (except movement) happened"""
        
        if self.length + 2 == len(self.field) ** 2:
            return {"happened": "win", "eaten": "none"}

        if self.OPPOSITE_DIRECTION[direction] == self.direction:
            direction = self.direction

        self.direction = direction

        match direction:
            case "right":
                return self.__go_right__()
            case "up":
                return self.__go_up__()
            case "left":
                return self.__go_left__()
            case "down":
                return self.__go_down__()
            case _:
                return {"happened": "crushed", "eaten": "none"}

    def create_apple(self, num_of_apples: int) -> None:
        apples = sum(
            cell.startswith("A")
            for row in self.field
            for cell in row
        )

        free_cells = [
            (x, y)
            for y, row in enumerate(self.field)
            for x, cell in enumerate(row)
            if cell == "N"
        ]

        missing = min(
            num_of_apples - apples,
            len(free_cells)
        )

        if missing <= 0:
            return

        for _ in range(missing):
            x, y = random.choice(free_cells)
            free_cells.remove((x, y))

            rng = random.randint(1, 100)

            if rng <= 70:
                apple = "AR"
            elif rng <= 95:
                apple = "AB"
            else:
                apple = "AP"

            self.field[y][x] = apple

    def __go_right__(self) -> dict[
                Literal["happened", "eaten"],
                Literal["nothing", "crushed", "win", "none", "red", "blue", "pink"]
                ]:

        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        eaten = "none"

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "L":
                        return {"happened": "nothing", "eaten": eaten}

                    if x + 1 >= len(self.field[0]):
                        return {"happened": "crushed", "eaten": eaten}
                    elif self.field[y][x + 1] != "N" and \
                            self.field[y][x + 1][0] != "A":
                        return {"happened": "nothing", "eaten": eaten}

                    grow = self.field[y][x + 1][0] == "A"

                    if facing != "R":
                        self.field[y][x] = f"T{facing}R"
                    else:
                        self.field[y][x] = "DR"
                    self.field[y][x + 1] = "HR"

                    if grow:
                        print(self.field[y][x][1])
                        match self.field[y][x][1]:
                            case "P":
                                eaten = "pink"
                            case "B":
                                eaten = "blue"
                            case "R":
                                eaten = "red"
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
        return {"happened": "nothing", "eaten": eaten}

    def __go_up__(self) -> dict[
                Literal["happened", "eaten"],
                Literal["nothing", "crushed", "win", "none", "red", "blue", "pink"]
                ]:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        eaten = "none"

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "D":
                        return {"happened": "nothing", "eaten": eaten}

                    if y - 1 < 0:
                        return {"happened": "crushed", "eaten": eaten}
                    elif self.field[y - 1][x] != "N" and \
                            self.field[y - 1][x][0] != "A": 
                        return {"happened": "crushed", "eaten": eaten}

                    grow = self.field[y - 1][x][0] == "A"

                    if facing != "U":
                        self.field[y][x] = f"T{facing}U"
                    else:
                        self.field[y][x] = "DU"
                    self.field[y - 1][x] = "HU"

                    if grow:
                        match self.field[y][x][1]:
                            case "P":
                                eaten = "pink"
                            case "B":
                                eaten = "blue"
                            case "R":
                                eaten = "red"
                        self.length += 1

                        break

                    match facing:
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
        return {"happened": "nothing", "eaten": eaten}

    def __go_left__(self) -> dict[
                Literal["happened", "eaten"],
                Literal["nothing", "crushed", "win", "none", "red", "blue", "pink"]
                ]:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        eaten = "none"

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "R":
                        return {"happened": "nothing", "eaten": eaten}

                    if x - 1 < 0:
                        return {"happened": "crushed", "eaten": eaten}
                    elif self.field[y][x - 1] != "N" and \
                            self.field[y][x - 1][0] != "A":
                        return {"happened": "crushed", "eaten": eaten}

                    grow = self.field[y][x - 1][0] == "A"

                    if facing != "L":
                        self.field[y][x] = f"T{facing}L"
                    else:
                        self.field[y][x] = "DL"
                    self.field[y][x - 1] = "HL"

                    if grow:
                        match self.field[y][x][1]:
                            case "P":
                                eaten = "pink"
                            case "B":
                                eaten = "blue"
                            case "R":
                                eaten = "red"
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
        return {"happened": "nothing", "eaten": eaten}

    def __go_down__(self) -> dict[
                Literal["happened", "eaten"],
                Literal["nothing", "crushed", "win", "none", "red", "blue", "pink"]
                ]:
        """Movement method. Returns True, if snake crushed"""
        x, y = self.head_x, self.head_y
        grow = False

        eaten = "none"

        while True:
            match self.field[y][x][0]:
                case "H":
                    facing = self.field[y][x][1]

                    if facing == "U":
                        return {"happened": "nothing", "eaten": eaten}

                    if y + 1 >= len(self.field):
                        return {"happened": "crushed", "eaten": eaten}
                    elif self.field[y + 1][x] != "N" and \
                            self.field[y + 1][x][0] != "A":
                        return {"happened": "crushed", "eaten": eaten}

                    grow = self.field[y + 1][x][0] == "A"

                    if facing != "D":
                        self.field[y][x] = f"T{facing}D"
                    else:
                        self.field[y][x] = "DD"
                    self.field[y + 1][x] = "HD"

                    if grow:
                        match self.field[y][x][1]:
                            case "P":
                                eaten = "pink"
                            case "B":
                                eaten = "blue"
                            case "R":
                                eaten = "red"
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
        return {"happened": "nothing", "eaten": eaten}
