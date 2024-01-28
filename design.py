import pygame
from Settings import Colors, Text, Window
pygame.font.init()
import edit

class buttons:
    
    def __init__(self, name, pos, dimensions, action, argument = None, border = 0, font = pygame.font.SysFont(Text.BUTTONS_FONT, Text.BUTTONS_FONT_SIZE), show = True, permanent = True, type = "default", old_x = None, old_w = None, FIELD_WIDTH = Window.WIDTH):
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
        if Window.BORDER == None:
            self.border = border
        else:
            self.border = Window.BORDER
        self.permanent = permanent
        self.type = type
        self.type_location = 0

    def draw(self, surface, mouse, offset, time, selected_field):
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":
            color = Colors.HOVER
        elif self == selected_field:
            color = Colors.SELECTED
        else:
            try:
                if self.type == "if":
                    color = Colors.IF_STATEMENT
                elif self.type == "if-dan":
                    color = Colors.IF_THAN
                elif self.type == "if-anders":
                    color = Colors.IF_ELSE
                elif self.type == "while":
                    color = Colors.WHILE_STATEMENT
                elif self.type == "function":
                    color = Colors.FUNCTION
                elif self.type == "if-sec-T":
                    color = Colors.SUB_IF_TRUE_STATEMENT
                elif self.type == "if-sec-F":
                    color = Colors.SUB_IF_FALSE_STATEMENT
                elif self.type == "while-sec":
                    color = Colors.SUB_WHILE_STATEMENT
                elif self.type == "function-sec":
                    color = Colors.SUB_FUNCTION
                else:
                    color = Colors.FIELD
            except:
                color = Colors.FIELD
        
        if not self.permanent:
            self.rect.y -= offset
        
        try:
            if self.type == "if":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.topright, self.rect.midbottom], self.border)
            elif self.type == "if-dan":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.bottomright, self.rect.bottomleft], self.border)
                pygame.draw.line(surface, Colors.IF_THAN_LINE, self.rect.topleft, self.rect.bottomright, Window.IF_LINE_WIDTH)
            elif self.type == "if-anders":
                pygame.draw.polygon(surface, color, [self.rect.bottomleft, self.rect.topright, self.rect.bottomright], self.border)
                pygame.draw.line(surface, Colors.IF_ELSE_LINE, self.rect.bottomleft, self.rect.topright, Window.IF_LINE_WIDTH)
            else:
                pygame.draw.rect(surface, color, self.rect, self.border, Window.ROUNDING)
        except:
            pygame.draw.rect(surface, color, self.rect, self.border, Window.ROUNDING)

        text = self.font.render(self.name, 1, Colors.TEXT)
        index = -1
        while text.get_width() > self.rect.width - 20:
            txt = self.name[0:index]
            text = self.font.render(txt, 1, Colors.TEXT)
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
                text = self.font.render(txt, 1, Colors.TEXT)
                counting = 0
                while mouse[0] < pos[0] + text.get_width():
                    txt = txt[:-1]
                    text = self.font.render(txt, 1, Colors.TEXT)
                self.type_location = len(txt)
                print(len(txt), self.type_location)
            token = self.font.render("|", 1, Colors.TEXT)
            surface.blit(token, (pos[0] + self.font.render(self.name[0:self.type_location], 1, Colors.TEXT).get_width(), pos[1]))

        if not self.permanent:
            self.rect.y += offset

        if self.rect.collidepoint(mouse):
            text = self.font.render(f"{self.name}, x:{self.rect.x}, y:{self.rect.y}", 1, Colors.TEXT)
            pos = (mouse[0], mouse[1] - offset)
            surface.blit(text, pos)

    def execute(self, mouse, FIELDS, selected_field, FIELD_WIDTH, WIDTH, HEIGHT, BUTTON, BACKUPS):
        if self.rect.collidepoint(mouse) and self.show:
            if self.argument in ["default", "while", "if", "function"]:
                temp = []
                temp.extend(FIELDS)
                BACKUPS.append(temp)
                FIELDS, selected_field = self.action(self.argument, FIELDS, selected_field, FIELD_WIDTH)
            elif self.argument != None:
                self.action(self.argument)
            else:
                print(self.action)
                if "load_json" in str(self.action):
                    FIELDS, WIDTH = self.action(FIELDS, WIDTH)
                elif "save_json" in str(self.action):
                    self.action(FIELDS, WIDTH)
                elif "save_image" in str(self.action):
                    self.action(FIELDS, WIDTH, selected_field, BUTTON, HEIGHT)
                elif "delete_field" in str(self.action):
                    temp = []
                    temp.extend(FIELDS)
                    BACKUPS.append(temp)
                    selected_field, FIELDS = self.action(selected_field, FIELDS)
                elif "load_backup" in str(self.action):
                    FIELDS, BACKUPS = self.action(FIELDS, BACKUPS)
                else:
                    self.action()
        print(FIELDS, BACKUPS)
        return FIELDS, selected_field, BACKUPS

class field(buttons):
    def __init__(self, name, pos, dimensions, type, old_x = None, old_w = None, border = 0, show=True, font = pygame.font.SysFont(Text.FIELDS_FONT, Text.FIELDS_FONT_SIZE)):
        super().__init__(name, pos, dimensions, "empty action", None, border, font, show, False, type, old_x, old_w)
        self.type = type
        
    def execute(self, mouse, selected_field):
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":
            selected_field = self
        return selected_field
    
    def typ(self, event, selected_field):
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
        return selected_field
