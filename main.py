import pygame
from Settings import Window, Text
import update_checker
import draw
from resize import window_size, update_button_possitions
import edit

WIDTH, HEIGHT = Window.WIDTH, Window.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(Window.TITLE)
FPS = Window.FPS
pygame.font.init()

BUTTON_FONT = pygame.font.SysFont(Text.BUTTONS_FONT, Text.BUTTONS_FONT_SIZE)
TEXT_FONT = pygame.font.SysFont(Text.FIELDS_FONT, Text.FIELDS_FONT_SIZE)

FIELDS = []
BUTTON = []
FIELD_WIDTH = WIDTH - 70


'''class buttons:
    
    def __init__(self, name, pos, dimensions, action, argument = None, border = 0, font = BUTTON_FONT, show = True, permanent = True, type = "default", old_x = None, old_w = None):
        self.rect = pygame.Rect(pos[0], pos[1], dimensions[0], dimensions[1])
        if old_x == None:
            self.old_x = pos[0]
        else:
            self.old_x = old_x
        if old_w == None:
            self.old_w = FIELD_WIDTH
        else:
            self.old_w = old_w
        self.name = name
        self.dimensions = dimensions
        self.action = action
        self.show = show
        self.font = font
        self.argument = argument
        if theme.BORDER == None:
            self.border = border
        else:
            self.border = theme.BORDER
        self.permanent = permanent
        self.type = type
        self.type_location = 0

    def draw(self, surface, mouse, offset, time):
        global selected_field
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":
            color = theme.HOVER
        elif self == selected_field:
            color = theme.SELECTED
        else:
            try:
                if self.type == "if":
                    color = theme.IF_STATEMENT
                elif self.type == "if-dan":
                    color = theme.IF_THAN
                elif self.type == "if-anders":
                    color = theme.IF_ELSE
                elif self.type == "while":
                    color = theme.WHILE_STATEMENT
                elif self.type == "function":
                    color = theme.FUNCTION
                elif self.type == "if-sec-T":
                    color = theme.SUB_IF_TRUE_STATEMENT
                elif self.type == "if-sec-F":
                    color = theme.SUB_IF_FALSE_STATEMENT
                elif self.type == "while-sec":
                    color = theme.SUB_WHILE_STATEMENT
                elif self.type == "function-sec":
                    color = theme.SUB_FUNCTION
                else:
                    color = theme.FIELD
            except:
                color = theme.FIELD
        
        if not self.permanent:
            self.rect.y -= offset
        
        try:
            if self.type == "if":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.topright, self.rect.midbottom], self.border)
            elif self.type == "if-dan":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.bottomright, self.rect.bottomleft], self.border)
            elif self.type == "if-anders":
                pygame.draw.polygon(surface, color, [self.rect.bottomleft, self.rect.topright, self.rect.bottomright], self.border)
            else:
                pygame.draw.rect(surface, color, self.rect, self.border, theme.ROUNDING)
        except:
            pygame.draw.rect(surface, color, self.rect, self.border, theme.ROUNDING)

        text = self.font.render(self.name, 1, theme.TEXT)
        index = -1
        while text.get_width() > self.rect.width - 20:
            txt = self.name[0:index]
            text = self.font.render(txt, 1, theme.TEXT)
            index -= 1

        if self.type == "if":
            pos = (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)
        elif self.type == "if-anders":
            pos = (self.rect.bottomright[0] - text.get_width() - 10, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)
        else:
            pos = (self.rect.x + 10, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)
        surface.blit(text, pos)

        if self == selected_field and time % 60 < 30:
            if pygame.mouse.get_pressed()[0] and pos[1] < mouse[1] < pos[1] + text.get_height():
                txt = self.name
                text = self.font.render(txt, 1, theme.TEXT)
                counting = 0
                while mouse[0] < pos[0] + text.get_width():
                    txt = txt[:-1]
                    text = self.font.render(txt, 1, theme.TEXT)
                self.type_location = len(txt)
                print(len(txt), self.type_location)
            token = self.font.render("|", 1, theme.TEXT)
            surface.blit(token, (pos[0] + self.font.render(self.name[0:self.type_location], 1, theme.TEXT).get_width(), pos[1]))

        if not self.permanent:
            self.rect.y += offset

        if self.rect.collidepoint(mouse):
            text = self.font.render(f"{self.name}, x:{self.rect.x}, y:{self.rect.y}", 1, theme.TEXT)
            pos = (mouse[0], mouse[1] - offset)
            surface.blit(text, pos)

    def execute(self, mouse):
        if self.rect.collidepoint(mouse) and self.show:
            if self.argument != None:
                self.action(self.argument)
            else:
                self.action()

class field(buttons):
    def __init__(self, name, pos, dimensions, type, old_x = None, old_w = None, border = 0, show=True, font = TEXT_FONT):
        super().__init__(name, pos, dimensions, "empty action", None, border, font, show, False, type, old_x, old_w)
        self.type = type
        
    def execute(self, mouse):
        global selected_field
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":
            selected_field = self
    
    def typ(self, event):
        if event.key == pygame.K_BACKSPACE:
            name = self.name
            self.name = self.name[0: selected_field.type_location]
            self.name = self.name[:-1]
            self.name += name[selected_field.type_location : len(name)]
            if selected_field.type_location > 0:
                selected_field.type_location -= 1
        elif event.key == pygame.K_LEFT:
            selected_field.type_location -= 1
        elif event.key == pygame.K_RIGHT:
            selected_field.type_location += 1
        else:
            name = self.name
            self.name = self.name[0: selected_field.type_location]
            temp = event.unicode
            self.name += temp
            self.name += name[selected_field.type_location : len(name)]
            selected_field.type_location += len(temp)

def make_new_field(type):
    global selected_field
    amount_added = 0
    height_added = 0
    old_x = 0
    old_w = 0
    try:
        if selected_field.type == "while" or selected_field.type == "if":
            hoogte = selected_field.rect.y
            breedte = selected_field.rect.x
            for item in FIELDS:
                if item.rect.y > hoogte and item.rect.x > breedte:
                    hoogte = item.rect.y
                    print("item", item.rect.y)
            hoogte += theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT
            start_pos = (breedte, hoogte)
            print("sel", selected_field.rect.topleft, "\nnew", start_pos)
            pass_type = type
        else:
            start_pos = (selected_field.rect.topleft[0], selected_field.rect.topleft[1] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT)
        
            if type == "default":
                pass_type = selected_field.type
            else:
                pass_type = type
        dimensions = (selected_field.rect.width, selected_field.rect.height)
        old_x = selected_field.old_x
        old_w = selected_field.old_w
        print(start_pos)
    except:
        hoogte = 10
        for veld in FIELDS:
            if veld.rect.y + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT > hoogte:
                hoogte = veld.rect.y + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT
        start_pos = (10, hoogte)
        dimensions = (FIELD_WIDTH, theme.FIELD_HEIGHT)
        old_x = 10
        old_w = FIELD_WIDTH
        pass_type = type

    try:
        print(f"dimensions field: {selected_field.dimensions}")
    except:
        pass
    print(f"dimensions are: {dimensions}")

    if type == "default":
        FIELDS.append(field(theme.DEFAULT_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), pass_type, old_x, old_w))
        amount_added = 1
        height_added = 1
    elif type == "if":
        FIELDS.append(field(theme.IF_STATEMENT_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), pass_type, old_x, old_w)),
        FIELDS.append(field(theme.IF_STATEMENT_LEFT, (start_pos[0] + theme.MARGIN_IF_STATEMENT_LEFT, start_pos[1] + 10), (dimensions[0] / 2 - 15, theme.FIELD_HEIGHT - 10), "if-dan", old_x + theme.MARGIN_IF_STATEMENT_LEFT, old_w / 2 - 15))
        FIELDS.append(field(theme.IF_STATEMENT_RIGHT, (start_pos[0] + dimensions[0] // 2 + 25, start_pos[1] + 5), (dimensions[0] / 2 - 15, theme.FIELD_HEIGHT - 5), "if-anders", old_x + old_w // 2 + 25, old_w / 2 - 15))
        FIELDS.append(field(theme.IF_STATEMENT_B_LEFT, (start_pos[0] + theme.MARGIN_IF_STATEMENT_LEFT, start_pos[1] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] / 2 - theme.MARGIN_IF_STATEMENT_LEFT/2 - theme.MARGIN_IF_STATEMENT_MIDDLE/2, theme.FIELD_HEIGHT), "if-sec-T", old_x + theme.MARGIN_IF_STATEMENT_LEFT, old_w / 2 - theme.MARGIN_IF_STATEMENT_LEFT/2 - theme.MARGIN_IF_STATEMENT_MIDDLE/2))
        FIELDS.append(field(theme.IF_STATEMENT_B_RIGHT, (start_pos[0] + dimensions[0] // 2 + theme.MARGIN_IF_STATEMENT_LEFT/2 + theme.MARGIN_IF_STATEMENT_MIDDLE/2, start_pos[1] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] / 2 - theme.MARGIN_IF_STATEMENT_MIDDLE/2 - theme.MARGIN_IF_STATEMENT_LEFT/2, theme.FIELD_HEIGHT), "if-sec-F", old_x + old_w // 2 + theme.MARGIN_IF_STATEMENT_LEFT/2 + theme.MARGIN_IF_STATEMENT_MIDDLE/2, old_w / 2 - theme.MARGIN_IF_STATEMENT_MIDDLE/2 - theme.MARGIN_IF_STATEMENT_LEFT/2))
        amount_added = 5
        height_added = 2
    elif type == "while":
        FIELDS.append(field(theme.WHILE_STATEMENT_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), type, old_x, old_w)),
        FIELDS.append(field(theme.WHILE_STATEMENT_LOWER_TEXT, (start_pos[0] + theme.MARGIN_WHILE_STATEMENT, start_pos[1] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] - theme.MARGIN_WHILE_STATEMENT, theme.FIELD_HEIGHT), "while-sec", old_x + theme.MARGIN_WHILE_STATEMENT, old_w - theme.MARGIN_WHILE_STATEMENT))
        
        amount_added = 3
        height_added = 2

    elif type == "function":
        FIELDS.append(field(theme.FUNCTION_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), type, 0, True, pygame.font.SysFont(theme.FIELDS_FONT, theme.FUNCTION_FONT_SIZE)))
        FIELDS.append(field(theme.FUNCTION_LOWER_TEXT, (start_pos[0] + 15, start_pos[0] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] - 30, dimensions[1]), "function-sec"))


    if selected_field != None:
        for i in range(len(FIELDS) - amount_added):
            item = FIELDS[i]
            if item.rect.y >= start_pos[1]:
                touch = False
                if start_pos[0] + dimensions[0] > item.rect.x >= start_pos[0] and item != selected_field:
                    touch = True
                if touch:
                    item.rect.y += (theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT) * height_added
                print(item.name, item.rect.y)

        selected_field = FIELDS[len(FIELDS) - 1]

def make_new_field(type):
    global FIELDS, selected_field
    FIELDS, selected_field = make.new_field(type, FIELDS, selected_field, FIELD_WIDTH)


def save_image():
    hoogte = 10
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y
    hoogte += 60
    print(hoogte)
    surface = pygame.Surface((WIDTH - 50, hoogte))
    
    draw.display(surface, (-10, -10), 0, 59, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)
    name = asksaveasfilename(initialfile=theme.SAVE_NAME_IMAGE, initialdir=theme.SAVE_DIR_IMAGE)
    if name != "":
        pygame.image.save(surface, f"{name}.png")

def save_json():
    save_fields = []
    for field in FIELDS:
        lijst = [field.name, field.rect.topleft, field.dimensions, field.type, field.border, field.show]
        save_fields.append(lijst)
    name = asksaveasfilename(initialfile=theme.SAVE_NAME_FILE, initialdir=theme.SAVE_DIR_FILE)
    if name != "":
        with open(f"{name}.json", "w") as file:
            dump(save_fields, file)

def load_json():
    global FIELDS
    file_selected = askopenfilename(filetypes=[("json", ".json")], initialfile=theme.LOAD_NAME_FILE, initialdir=theme.LOAD_DIR_FILE)
    try:
        print(file_selected)
        with open(file_selected, "r") as file:
            save_fields = load(file)
        FIELDS = []
        for item in save_fields:
            FIELDS.append(field(item[0], item[1], item[2], item[3], item[4], item[5]))
    except:
        pass
    print(FIELDS)

def draw_side_lines(surface, offset, start, color):
    hoogte = 0
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y

    repetition = hoogte + 10
    for breedte in range(start, WIDTH - 50, theme.WIDTH_SIDEBAR_WHILE_STATEMENT):
        blocks = []
        for i in range(10, repetition, theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT):
            rect = pygame.Rect(breedte, i - offset, theme.WIDTH_SIDEBAR_WHILE_STATEMENT, theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT + 10)
            collision = False
            source = None
            for item in FIELDS:
                comp_rect = pygame.Rect(item.rect.x, item.rect.y - offset, item.rect.width, item.rect.height)
                #pygame.draw.rect(surface, color, rect)
                if comp_rect.colliderect(rect):
                    if item.type != "while":
                        collision = True
                    if item.type == "while":
                        source = item
                    
            if not collision:
                if source != None:
                    rect = pygame.Rect(source.rect.x, rect.y, rect.width, rect.height)
                    pygame.draw.rect(surface, theme.WHILE_STATEMENT, rect, theme.BORDER, theme.ROUNDING)
                    blocks.append(rect)
                else:
                    for block in blocks:
                        if block.colliderect(rect):
                            rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                            pygame.draw.rect(surface, theme.WHILE_STATEMENT, rect, theme.BORDER, theme.ROUNDING)
                            blocks.append(rect)
                            break

def draw_lines(surface, sort):
    if sort == "fancy_lines":
        for i in range(0, WIDTH, 10):
            pygame.draw.line(surface, theme.BACKGROUND_LINE_COLOR, (i, HEIGHT - i), (WIDTH - i, i))
    elif sort == "triangle_lines":
        for i in range(0, WIDTH, 10):
            pygame.draw.line(surface, theme.BACKGROUND_LINE_COLOR, (i, HEIGHT), (WIDTH - i, 0))
    elif sort == "diagonal_lines":
        for i in range(0, WIDTH*2, 10):
            pygame.draw.line(surface, theme.BACKGROUND_LINE_COLOR, (-1 * WIDTH + i, HEIGHT), (i, 0))
    elif sort == "no_lines":
        pass

def draw_display(finale_surface, mouse, offset, time):
    surface = pygame.Surface((finale_surface.get_width(), finale_surface.get_height()))
    surface.fill(theme.BACKGROUND)
    draw_lines(surface, theme.BACKGROUND_PATERN)
    #draw_side_lines(surface, offset, theme.WIDTH_SIDEBAR_WHILE_STATEMENT, (200, 200, 200))
    draw_side_lines(surface, offset, 10 - theme.WIDTH_SIDEBAR_WHILE_STATEMENT, (200, 100, 50))
    
    counting = 0
    for item in FIELDS:
        item.draw(surface, mouse, offset, time, selected_field)
        counting += 1
    for item in BUTTON:
        item.draw(surface, (mouse[0], mouse[1] - offset), 0, time, selected_field)

    finale_surface.blit(surface, (0, 0))
    pygame.display.update()

def delete_field():
    global selected_field
    removed = 0
    selected_hoogte = selected_field.rect.y
    if selected_field.type == "while" or selected_field.type == "if":
        hoogte = selected_field.rect.y
        max_hoogte = selected_field.rect.y
        breedte = selected_field.rect.x
        fields_rm = [selected_field]
        for field in FIELDS:
            if field.rect.y > hoogte and field.rect.x <= breedte and field != selected_field:
                hoogte = field.rect.y
            if field.rect.y > max_hoogte:
                max_hoogte = field.rect.y
        print(hoogte)
        if hoogte == selected_field.rect.y:
            hoogte = max_hoogte + 10
        for field in FIELDS:
            if selected_field.rect.y <= field.rect.y < hoogte and field.rect.x > breedte and field:
                fields_rm.append(field)
        removed = len(fields_rm)
        print(fields_rm)
        for field in fields_rm:
            FIELDS.remove(field)
    elif True:
        FIELDS.remove(selected_field)
        removed = 1

    for i in range(removed):
        for field in FIELDS:
            if field.rect.y > selected_hoogte:
                field.rect.y -= theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT
                for item in FIELDS:
                    if item != field and item.rect.colliderect(field.rect):
                        field.rect.y += theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT
                        break
    selected_field = None
    
def window_size():
    global WIDTH, HEIGHT, FIELD_WIDTH
    nwidth = WIN.get_width()
    nheight = WIN.get_height()
    if nwidth != WIDTH:
        change_field_width(nwidth - 70)
        WIDTH = nwidth
        FIELD_WIDTH = WIDTH - 70
        update_button_possitions()
    if nheight != HEIGHT:
        HEIGHT = nheight
        update_button_possitions()

def update_button_possitions():
    global BUTTON
    BUTTON = []
    BUTTON.append(buttons(theme.FIELD_DEFAULT, (WIDTH - 50, 10), (40, 40), make_new_field, "default"))
    BUTTON.append(buttons(theme.FIELD_IF_STATEMENT, (WIDTH - 50, 60), (40, 40), make_new_field, "if"))
    BUTTON.append(buttons(theme.FIELD_WHILE_STATEMENT, (WIDTH - 50, 110), (40, 40), make_new_field, "while"))
    BUTTON.append(buttons(theme.FIELD_FUNCTION, (WIDTH - 50, 160), (40, 40), make_new_field, "function"))
    BUTTON.append(buttons(theme.SAVE_AS_JSON, (WIDTH - 50, HEIGHT - 50), (40, 40), save_json, None))
    BUTTON.append(buttons(theme.SAVE_AS_IMAGE, (WIDTH - 50, HEIGHT - 100), (40, 40), save_image, None))
    BUTTON.append(buttons(theme.LOAD_JSON, (WIDTH - 50, HEIGHT - 150), (40, 40), load_json, None))
    BUTTON.append(buttons(theme.FIELD_DELETE, (WIDTH - 50, 210), (40, 40), delete_field, None))

def change_field_width(new_field_width):
    lines = {}
    for field in FIELDS:
        if not field.rect.y in lines:
            lines[field.rect.y] = [[field.rect.x, field]]
        else:
            lines[field.rect.y].append([field.rect.x, field])

    old_x = {}

    for i, line in enumerate(lines.values()):
        lijst = sorted(line, key=lambda l:l[0])
        offset = 0
        for field in lijst:
            print()
            print(old_x)
            print()
            print(field[1].rect)
            old_width = field[1].rect.width
            field[1].rect.width = field[1].rect.width * ((new_field_width / (WIDTH - 70)))
            old_x_pos = field[1].rect.x
            try:
                off = old_x[field[1].old_x]
                field[1].rect.x = off
                print(field[1].type)
                print(field[1].name)
                print(field[1].rect)
            except:
                old = field[1].rect.x
                field[1].rect.x = field[1].rect.x + offset
                
                special = ["if-dan", "if-anders", "placeholder", "if-sec-F"]
                if field[1].type in special:
                    main = FIELDS[FIELDS.index(field[1]) - special.index(field[1].type) - 1]
                    if field[1].type in ["if-dan", "if-sec-T"]:
                        field[1].rect.x = main.rect.x + theme.MARGIN_IF_STATEMENT_LEFT
                    if field[1].type in ["if-dan", "if-anders"]:
                        field[1].rect.width = main.rect.width / 2 - 15
                    if field[1].type in ["if-anders"]:
                        field[1].rect.x = main.rect.x + main.rect.width/2 + 25
                    if field[1].type in ["if-sec-T", "if-sec-F"]:
                        field[1].rect.width = main.rect.width / 2 - theme.MARGIN_IF_STATEMENT_LEFT / 2 - theme.MARGIN_IF_STATEMENT_MIDDLE / 2
                    if field[1].type in ["if-sec-F"]:
                        pre = FIELDS[FIELDS.index(field[1]) - 1]
                        field[1].rect.x = pre.rect.x + pre.rect.width + theme.MARGIN_IF_STATEMENT_MIDDLE
                if field[1].type == "while-sec":
                    main = FIELDS[FIELDS.index(field[1]) - 1]
                    field[1].rect.x = main.rect.x + theme.MARGIN_WHILE_STATEMENT
                old_x[field[1].old_x] = field[1].rect.x

                print(field[1].type)
                print(field[1].rect)
                print(field[1].name)
                print(field[1].old_x)
            
            offset += field[1].rect.width + field[1].rect.x - old_width - old_x_pos'''

def main():
    global selected_field
    global WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS
    active_time = 0
    run = True
    clock = pygame.time.Clock()
    selected_field = None
    offset = 0
    BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)
    BACKUPS = []

    while run:
        clock.tick(FPS)
        active_time += 1
        if active_time % FPS == 0:
            WIDTH, HEIGHT, FIELD_WIDTH, BUTTON = window_size(WIN, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS)
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0], mouse[1] + offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in BUTTON:
                    FIELDS, selected_field, BACKUPS = item.execute((mouse[0], mouse[1] - offset), FIELDS, selected_field, FIELD_WIDTH, WIDTH, HEIGHT, BUTTON, BACKUPS)
                selected_field = None
                for button in FIELDS:
                    selected_field = button.execute(mouse, selected_field)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE and selected_field != None:
                   selected_field, FIELDS = edit.delete_field(selected_field, FIELDS)
                if selected_field != None:
                    selected_field = selected_field.typ(event, selected_field)

            if event.type == pygame.MOUSEWHEEL:
                offset -= event.y * Window.CHANGE_Y_POS
            
            if len(BACKUPS) > 10:
                BACKUPS.pop(0)
        draw.display(WIN, mouse, offset, active_time, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)

    pygame.quit()


if __name__ == "__main__":
    main()
