#importing files
import resize
from Settings import SaveAndLoad, Window
import pygame
from tkinter.filedialog import asksaveasfilename, askopenfilename
import draw
from json import dump, load

#function to save the diagram as an image (.png)
def save_image(FIELDS, WIDTH, selected_field, BUTTON, HEIGHT):

    #getting the height of all fields
    hoogte = 10
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y
    hoogte += Window.FIELD_HEIGHT + 10
    print(hoogte)

    #making a surface
    surface = pygame.Surface((WIDTH - 50, hoogte))
    
    #drawing all the fields to the surface
    draw.display(surface, (-10, -10), 0, 59, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)
    
    #asking for a file name and location
    name = asksaveasfilename(initialfile=SaveAndLoad.SAVE_NAME_IMAGE, initialdir=SaveAndLoad.SAVE_DIR_IMAGE)

    #saving the image
    if name != "":
        pygame.image.save(surface, f"{name}.png")

#function to save the diagram as a json file (.json), this function is also used to make a backup
def save_json(FIELDS, WIDTH, popup=True):

    #remebering the width the screen had at the time of saving
    save_fields = [WIDTH]

    #adding all essential parameters for each field to the save list
    for field in FIELDS:
        lijst = [field.name, field.rect.topleft, field.dimensions, field.type, field.old_x, field.old_w, field.border]
        save_fields.append(lijst)

    #if the file needs to be stored (not when making a backup)
    if popup:

        #get a filename from the user
        name = asksaveasfilename(initialfile=SaveAndLoad.SAVE_NAME_FILE, initialdir=SaveAndLoad.SAVE_DIR_FILE)
        if name != "":

            #dumping the save_fields list in the file as json information
            with open(f"{name}.json", "w") as file:
                dump(save_fields, file)

    return save_fields

#loading a save file, also used for loading a backup
def load_json(FIELDS, WIDTH, popup=True, change=True):

    #import needs to be here because design imports the saveload.save_json() function
    from design import field

    #if you are loading a file (not a backup), get the file name
    if popup:
        file_selected = askopenfilename(filetypes=[("json", ".json")], initialfile=SaveAndLoad.LOAD_NAME_FILE, initialdir=SaveAndLoad.LOAD_DIR_FILE)
        print(file_selected)
    else:
        file_selected = FIELDS
    try:
        #if loading a file
        if popup:
            #load the json data from the file
            print("file", file_selected)
            with open(file_selected, "r") as file:
                save_fields = load(file)

        #if you are loading a backup, the fields are equal to the backup
        else:
            save_fields = FIELDS

        print("loaded", save_fields)
        FIELDS = []
        width_s = save_fields.pop(0)
        FIELDS = []

        #load all the fields from the save_fields list
        for item in save_fields:
            FIELDS.append(field(item[0], item[1], item[2], item[3], item[4], item[5], item[6])) #name, pos, dimensions, type, old_x = None, old_w = None, border = 0, show=True, font = pygame.font.SysFont(theme.FIELDS_FONT, theme.FIELDS_FONT_SIZE)
    except:
        width_s = WIDTH
    print(FIELDS)

    #resize all the fields to the current window width
    if change:
        resize.change_field_width(WIDTH - 70, FIELDS, width_s)

    return FIELDS, width_s
