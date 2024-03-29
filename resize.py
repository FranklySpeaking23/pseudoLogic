#importing files
import pygame
from design import buttons
import make
import saveload
import edit
import other
from dev import log, load_settings

SETTINGS = load_settings()

#function to check if the size of the window changed and take the needed actions
def window_size(WIN, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS):

    #get the current dimensions
    nwidth = WIN.get_width()
    nheight = WIN.get_height()

    #if the width changed
    if nwidth != WIDTH:
        log("Width changed", "log")
        #change the width of the fields
        change_field_width(nwidth - 70, FIELDS, WIDTH)

        WIDTH = nwidth
        FIELD_WIDTH = WIDTH - 70

        #update the possitions of the buttons
        BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)

    #if the height changed
    if nheight != HEIGHT:
        log("Height changed", "log")
        HEIGHT = nheight

        #change the positions of the buttons
        BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)

    return WIDTH, HEIGHT, FIELD_WIDTH, BUTTON

#function to update the possitions of the buttons
def update_button_possitions(BUTTON, WIDTH, HEIGHT):
    log("Updating buttons", "func-s")
    #remove all buttons
    BUTTON = []

    #make all the buttons
    BUTTON.append(buttons(SETTINGS["text"]["button"]["default"], (WIDTH - 50, 10), (40, 40), make.new_field, "default"))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["if"], (WIDTH - 50, 60), (40, 40), make.new_field, "if"))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["while"], (WIDTH - 50, 110), (40, 40), make.new_field, "while"))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["shift"], (210, HEIGHT - 50), (40, 40), other.shift, None, image=SETTINGS["image"]["shift"], type="button_shift"))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["save_json"], (WIDTH - 50, HEIGHT - 50), (40, 40), saveload.save_json, None, image=SETTINGS["image"]["save_json"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["save_image"], (WIDTH - 50, HEIGHT - 100), (40, 40), saveload.save_image, None, image=SETTINGS["image"]["save_image"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["load_json"], (WIDTH - 50, HEIGHT - 150), (40, 40), saveload.load_json, None, image=SETTINGS["image"]["load_json"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["delete"], (60, HEIGHT - 50), (40, 40), edit.delete_field, None, image=SETTINGS["image"]["delete"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["back"], (10, HEIGHT - 50), (40, 40), edit.load_backup, None, image=SETTINGS["image"]["back"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["copy"], (110, HEIGHT - 50), (40, 40), edit.copy, None, image=SETTINGS["image"]["copy"]))
    BUTTON.append(buttons(SETTINGS["text"]["button"]["paste"], (160, HEIGHT - 50), (40, 40), edit.paste, None, image=SETTINGS["image"]["paste"]))

    log("Updating buttons", "func-e")
    return BUTTON

#function for changing the width of fields
def change_field_width(new_field_width, FIELDS, WIDTH):
    log("Updating field size", "func-s")

    #making a library with all the fields sorted per y position
    lines = {}
    for field in FIELDS:
        if not field.rect.y in lines:
            lines[field.rect.y] = [[field.rect.x, field]]
        else:
            lines[field.rect.y].append([field.rect.x, field])
    myKeys = list(lines.keys())
    myKeys.sort()
    sorted_dict = {i: lines[i] for i in myKeys}
    lines = sorted_dict

    #declaring variables
    old_x = {}
    adjusted = []

    #iterating through the different lines
    for i, line in enumerate(lines.values()):

        #sorting the line based on the fields their x pos
        lijst = sorted(line, key=lambda l:l[0])
        offset = 0

        #iterating through the fields
        for field in lijst:


            #changing the width of the field
            old_width = field[1].rect.width
            field[1].rect.width = field[1].rect.width * ((new_field_width / (WIDTH - 70)))

            #changing the x pos
            old_x_pos = field[1].rect.x
            try:

                #trying to load the x pos from already changed fields with the same x pos
                off = old_x[field[1].old_x]
                field[1].rect.x = off


            #if the x possition hasn't been used already
            except:
                old = field[1].rect.x
                field[1].rect.x = field[1].rect.x + offset
                
                #in special cases, move the x possition based on a previous fields
                special = ["if-dan", "if-anders", "placeholder", "if-sec-F"]
                if field[1].type in special:
                    main = FIELDS[FIELDS.index(field[1]) - special.index(field[1].type) - 1]

                    #I know that there are to much if statements here, but I'm lazy so won't remove them
                    if field[1].type in ["if-dan", "if-sec-T"]:
                        field[1].rect.x = main.rect.x + SETTINGS["field"]["margin_if_left"]
                    if field[1].type in ["if-dan", "if-anders"]:
                        field[1].rect.width = main.rect.width // 2 - SETTINGS["field"]["margin_if_middle"] //2 - SETTINGS["field"]["margin_if_left"] // 2
                    if field[1].type in ["if-anders"]:
                        field[1].rect.x = main.rect.x + main.rect.width - field[1].rect.width# + (main.rect.width - SETTINGS["field"]["margin_if_left"] - SETTINGS["field"]["margin_if_middle"]) // 2 + SETTINGS["field"]["margin_if_left"] + SETTINGS["field"]["margin_if_middle"]
                    if field[1].type in ["if-sec-T", "if-sec-F"]:
                        field[1].rect.width = main.rect.width // 2 - SETTINGS["field"]["margin_if_left"] // 2 - SETTINGS["field"]["margin_if_middle"] // 2
                    if field[1].type in ["if-sec-F"]:
                        pre = FIELDS[FIELDS.index(field[1]) - 1]
                        field[1].rect.x = pre.rect.x + pre.rect.width + SETTINGS["field"]["margin_if_middle"]
                #changing the inner part of a while statement based on the possition of it's parrent
                if field[1].type == "while-sec":
                    main = FIELDS[FIELDS.index(field[1]) - 1]
                    field[1].rect.x = main.rect.x + SETTINGS["field"]["margin_while"]

                #adding the old x pos to the old_x dictionary for the following fields
                old_x[field[1].old_x] = field[1].rect.x
            
            #adjusting the width to match the one from the parent
            try:
                if field[1].type in ["if-dan", "if-anders"]:
                            if field[1].type == "if-dan":
                                main = FIELDS[FIELDS.index(field[1]) - 1]
                            elif field[1].type == "if-anders":
                                main = FIELDS[FIELDS.index(field[1]) - 2]
                            field[1].rect.width = main.rect.width // 2 - SETTINGS["field"]["margin_if_middle"] //2 - SETTINGS["field"]["margin_if_left"] // 2
                if field[1].type in ["if-sec-T", "if-sec-F"]:
                            if field[1].type == "if-sec-T":
                                main = FIELDS[FIELDS.index(field[1]) - 3]
                            elif field[1].type == "if-sec-F":
                                main = FIELDS[FIELDS.index(field[1]) - 4]
                            field[1].rect.width = main.rect.width // 2 - SETTINGS["field"]["margin_if_left"] // 2 - SETTINGS["field"]["margin_if_middle"] // 2
            except:
                 pass
            if field[1].type == "if-anders":
                field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 2].rect.x + FIELDS[FIELDS.index(field[1]) - 2].rect.width - field[1].rect.x
            elif field[1].type == "if-sec-F" and FIELDS[FIELDS.index(field[1]) - 4].type == "if":
                field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 4].rect.x + FIELDS[FIELDS.index(field[1]) - 4].rect.width - field[1].rect.x
            elif field[1].type == "while-sec" and FIELDS[FIELDS.index(field[1]) - 1].type == "while":
                field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 1].rect.x + FIELDS[FIELDS.index(field[1]) - 1].rect.width - field[1].rect.x
            #elif field[1].type == "if-sec-F":
            #    field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 4].rect.x + FIELDS[FIELDS.index(field[1]) - 4].rect.width - field[1].rect.x
            #elif field[1].type == "while-sec":
            #    field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 1].rect.x + FIELDS[FIELDS.index(field[1]) - 1].rect.width - field[1].rect.x
            else:
                #making sure that all the fields underneath each other have the same width
                for place in adjusted:
                    if place.old_x == field[1].old_x and place.old_w == field[1].old_w:
                        field[1].rect.width = place.rect.width

            #adding the field to the adjusted fields list
            adjusted.append(field[1])
            offset += field[1].rect.width + field[1].rect.x - old_width - old_x_pos
        
    log("Updating field size", "func-e")
