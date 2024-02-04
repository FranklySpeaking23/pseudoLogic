import resize
from Settings import SaveAndLoad
import pygame
from tkinter.filedialog import asksaveasfilename, askopenfilename
import draw
from json import dump, load
from os import getlogin

def save_image(FIELDS, WIDTH, selected_field, BUTTON, HEIGHT):
    hoogte = 10
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y
    hoogte += 60
    print(hoogte)
    surface = pygame.Surface((WIDTH - 50, hoogte))
    
    draw.display(surface, (-10, -10), 0, 59, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)
    
    '''line = 0
    pos = 0
    code = f"The username of the person who made this image is: {getlogin()}. If the submision is from someone else, they probably copied the code".encode("utf-8")
    print(code)
    with open("test.txt", "w") as file:
        file.write(str(code))
    for i in range(0, len(code), 3):
        if pos > surface.get_width():
            pos = 0
            line += 1
        try:
            color = (code[i], code[i+1], code[i+2])
        except:
            try:
                color = (code[i], code[i+1], 0)
            except:
                color = (code[i], 0, 0)
        print(color)
        surface.set_at((pos, line), color)'''
    name = asksaveasfilename(initialfile=SaveAndLoad.SAVE_NAME_IMAGE, initialdir=SaveAndLoad.SAVE_DIR_IMAGE)
    if name != "":
        pygame.image.save(surface, f"{name}.png")

def save_json(FIELDS, WIDTH, popup=True):
    save_fields = [WIDTH]
    for field in FIELDS:
        lijst = [field.name, field.rect.topleft, field.dimensions, field.type, field.old_x, field.old_w, field.border]
        save_fields.append(lijst)
    if popup:
        name = asksaveasfilename(initialfile=SaveAndLoad.SAVE_NAME_FILE, initialdir=SaveAndLoad.SAVE_DIR_FILE)
        if name != "":
            with open(f"{name}.json", "w") as file:
                dump(save_fields, file)
    return save_fields

def load_json(FIELDS, WIDTH, popup=True):
    from design import field
    if popup:
        file_selected = askopenfilename(filetypes=[("json", ".json")], initialfile=SaveAndLoad.LOAD_NAME_FILE, initialdir=SaveAndLoad.LOAD_DIR_FILE)
        print(file_selected)
    else:
        file_selected = FIELDS
    try:
        if popup:
            print("file", file_selected)
            with open(file_selected, "r") as file:
                save_fields = load(file)
        else:
            save_fields = FIELDS
        print("loaded", save_fields)
        FIELDS = []
        width_s = save_fields.pop(0)
        FIELDS = []
        for item in save_fields:
            FIELDS.append(field(item[0], item[1], item[2], item[3], item[4], item[5], item[6])) #name, pos, dimensions, type, old_x = None, old_w = None, border = 0, show=True, font = pygame.font.SysFont(theme.FIELDS_FONT, theme.FIELDS_FONT_SIZE)
    except:
        width_s = WIDTH
    print(FIELDS)

    resize.change_field_width(WIDTH - 70, FIELDS, width_s)

    return FIELDS, width_s
