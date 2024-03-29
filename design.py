#importing files
from saveload import save_json
import pygame
from edit import check_prop
pygame.font.init()
from colorama import Fore, Style
from dev import load_settings

SETTINGS = load_settings()

#class for the buttons and second class for the fields
class buttons:
    
    #initializing a button
    def __init__(self, name, pos, dimensions, action, argument = None, border = 0, font = pygame.font.SysFont(SETTINGS["text"]["font"]["button_font"], SETTINGS["text"]["font"]["button_font_size"]), show = True, permanent = True, type = "default", old_x = None, old_w = None, FIELD_WIDTH = SETTINGS["window"]["width"], image=None):
        
        #making the rect
        self.rect = pygame.Rect(pos[0], pos[1], dimensions[0], dimensions[1])

        #setting old dimensions
        if old_x == None:
            self.old_x = pos[0]
        else:
            self.old_x = old_x
        if old_w == None:
            self.old_w = FIELD_WIDTH
        else:
            self.old_w = old_w

        #setting other information
        self.name = name
        self.dimensions = dimensions
        self.action = action
        self.show = show
        self.font = font
        self.argument = argument
        if SETTINGS["field"]["border"] == None:
            self.border = border
        else:
            self.border = SETTINGS["field"]["border"]
        self.permanent = permanent
        self.type = type
        self.type_location = 0
        if image != None:
            self.image = pygame.image.load(image)

    #drawing the button
    def draw(self, surface, mouse, offset, time, selected_field, SHIFT):

        #setting the color

        #hover over button
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":
            color = SETTINGS["color"]["hover"]

        #selected button
        elif self == selected_field:
            color = SETTINGS["color"]["selected"]

        elif self.type == "button_shift" and SHIFT:
            color = SETTINGS["color"]["shift_selected"]

        #based on type
        else:
            try:
                if self.type == "if":
                    color = SETTINGS["color"]["if"]
                elif self.type == "if-dan":
                    color = SETTINGS["color"]["if_than"]
                elif self.type == "if-anders":
                    color = SETTINGS["color"]["if_else"]
                elif self.type == "while":
                    color = SETTINGS["color"]["while"]
                elif self.type == "if-sec-T":
                    color = SETTINGS["color"]["sub_if_than"]
                elif self.type == "if-sec-F":
                    color = SETTINGS["color"]["sub_if_else"]
                elif self.type == "while-sec":
                    color = SETTINGS["color"]["sub_while"]
                else:
                    color = SETTINGS["color"]["field"]
            except:
                color = SETTINGS["color"]["field"]
        
        #adjusting the position to the offset
        if not self.permanent:
            self.rect.y -= offset
        
        #draw the button/field
        try:
            #special triangles for the if-, if-dan- and if-anders-statements
            if self.type == "if":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.topright, self.rect.midbottom], self.border)
            elif self.type == "if-dan":
                pygame.draw.polygon(surface, color, [self.rect.topleft, self.rect.bottomright, self.rect.bottomleft], self.border)
                pygame.draw.line(surface, SETTINGS["color"]["if_than_line"], self.rect.topleft, self.rect.bottomright, SETTINGS["field"]["width_if_line"])
            elif self.type == "if-anders":
                pygame.draw.polygon(surface, color, [self.rect.bottomleft, self.rect.topright, self.rect.bottomright], self.border)
                pygame.draw.line(surface, SETTINGS["color"]["if_else_line"], self.rect.bottomleft, self.rect.topright, SETTINGS["field"]["width_if_line"])
            else:
                #draw the rectangle for other buttons/fields
                pygame.draw.rect(surface, color, self.rect, self.border, SETTINGS["field"]["rounding"])
        except:
            pygame.draw.rect(surface, color, self.rect, self.border, SETTINGS["field"]["rounding"])

        try:
            surface.blit(self.image, self.rect.topleft)
        except:
            pass

        #render the text of the button/field
        text = self.font.render(self.name, 1, SETTINGS["color"]["text"])
        index = -1

        #changing the amount of characters that get shown based on the width that is available
        while text.get_width() > self.rect.width - 20:
            if abs(index) >= len(self.name):
                break
            txt = self.name[0:index]
            text = self.font.render(txt, 1, SETTINGS["color"]["text"])
            index -= 1

        #possitioning the text based on the type of the button/field
        if self.type == "if":
            pos = (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)
        elif self.type == "if-anders":
            pos = (self.rect.bottomright[0] - text.get_width() - 10, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)
        else:
            pos = (self.rect.x + 10, self.rect.y + self.dimensions[1] / 2 - text.get_height()/2)

        #drawing the text
        surface.blit(text, pos)

        #moving the cursor using the mouse
        if self == selected_field:
            if pygame.mouse.get_pressed()[0] and pos[1] < mouse[1] < pos[1] + text.get_height():
                txt = self.name
                text = self.font.render(txt, 1, SETTINGS["color"]["text"])
                counting = 0
                while mouse[0] < pos[0] + text.get_width():
                    if len(self.name) < counting:
                        break
                    txt = txt[:-1]
                    counting += 1
                    text = self.font.render(txt, 1, SETTINGS["color"]["text"])
                self.type_location = len(txt)

        #drawing the cursor
        if self == selected_field and time % 60 < 30:
            token = self.font.render("|", 1, SETTINGS["color"]["text"])
            surface.blit(token, (pos[0] + self.font.render(self.name[0:self.type_location], 1, SETTINGS["color"]["text"]).get_width(), pos[1]))

        #readding the offset to the y possition
        if not self.permanent:
            self.rect.y += offset

        #writing the text underneath the mouse
        '''if self.rect.collidepoint(mouse):
            text = self.font.render(f"{self.name}, x:{self.rect.x}, y:{self.rect.y}", 1, SETTINGS["color"]["text"])
            pos = (mouse[0], mouse[1] - offset)
            surface.blit(text, pos)'''

    #the action of a button
    def execute(self, mouse, FIELDS, selected_field, FIELD_WIDTH, WIDTH, HEIGHT, BUTTON, BACKUPS, COPY, SHIFT):

        #check collision of mouse and button
        if self.rect.collidepoint(mouse) and self.show:
            
            #if making a new field
            if self.argument in ["default", "while", "if", "function"]:

                #make a new backup
                temp = []
                temp.extend(FIELDS)
                temp = save_json(temp, WIDTH, False)
                BACKUPS.append(temp)

                #execute the action
                FIELDS, selected_field = self.action(self.argument, FIELDS, selected_field, FIELD_WIDTH, shift=SHIFT)

            #executing a function with parameter
            elif self.argument != None:
                self.action(self.argument)

            #special cases
            else:
                if "load_json" in str(self.action):
                    FIELDS, WIDTH = self.action(FIELDS, WIDTH)
                elif "save_json" in str(self.action):
                    self.action(FIELDS, WIDTH)
                elif "save_image" in str(self.action):
                    self.action(FIELDS, WIDTH, selected_field, BUTTON, HEIGHT)
                elif "delete_field" in str(self.action):

                    #making a backup before deleting fields
                    temp = []
                    temp.extend(FIELDS)
                    BACKUPS.append(temp)
                    selected_field, FIELDS = self.action(selected_field, FIELDS)
                elif "load_backup" in str(self.action):
                    FIELDS, BACKUPS = self.action(FIELDS, BACKUPS, WIDTH)
                elif "copy" in str(self.action):
                    COPY = self.action(FIELDS, selected_field, COPY)
                elif "paste" in str(self.action):
                    FIELDS = self.action(FIELDS, selected_field, COPY, WIDTH)
                elif "shift" in str(self.action):
                    SHIFT = self.action(SHIFT)
                else:
                    self.action()

        return FIELDS, selected_field, BACKUPS, COPY, SHIFT

#main class for the fields
class field(buttons):

    #initializing the field
    def __init__(self, name, pos, dimensions, type, old_x = None, old_w = None, border = 0, show=True, font = pygame.font.SysFont(SETTINGS["text"]["font"]["field_font"], SETTINGS["text"]["font"]["field_font_size"])):

        #initialize the parent class: buttons
        super().__init__(name, pos, dimensions, "empty action", None, border, font, show, False, type, old_x, old_w)

        #setting variables
        self.type = type
        
    #alternative execute function to the parent button.execute() function
    def execute(self, mouse, selected_field):

        #checking collision and excluding the if-dan and if-anders types
        if self.rect.collidepoint(mouse) and self.type != "if-dan" and self.type != "if-anders":

            #changig the selected field
            selected_field = self
            self.show = True

        if SETTINGS["window"]["logs"] and self.rect.collidepoint(mouse):
            print(f"{Fore.BLUE}field = (\n[type] {self.type}\n[name] {self.name}\n[rect] {self.rect}\n[old] ({self.old_x},{self.old_w})\n){Style.RESET_ALL}")

        return selected_field
    
    #type in field
    def typ(self, event, selected_field):

        #checking backspace
        if event.key == pygame.K_BACKSPACE:

            #removing character
            name = self.name
            self.name = self.name[0: selected_field.type_location]
            self.name = self.name[:-1]
            self.name += name[selected_field.type_location : len(name)]

            #changing the cursor location
            if selected_field.type_location > 0:
                selected_field.type_location -= 1

        #checking movement of cursor with arrow keys
        elif event.key == pygame.K_LEFT:
            selected_field.type_location -= 1
        elif event.key == pygame.K_RIGHT:
            selected_field.type_location += 1

        #adding character to field
        else:
            
            #adding character on the correct location
            name = self.name
            self.name = self.name[0: selected_field.type_location]
            temp = event.unicode
            self.name += temp
            self.name += name[selected_field.type_location : len(name)]

            #moving the cursor
            selected_field.type_location += len(temp)

            check_prop(self)

        return selected_field
