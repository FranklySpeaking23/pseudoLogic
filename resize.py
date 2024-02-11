#importing files
import pygame
from design import buttons
from Settings import Text, Window
import make
import saveload
import edit

#function to check if the size of the window changed and take the needed actions
def window_size(WIN, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS):

    #get the current dimensions
    nwidth = WIN.get_width()
    nheight = WIN.get_height()

    #if the width changed
    if nwidth != WIDTH:

        #change the width of the fields
        change_field_width(nwidth - 70, FIELDS, WIDTH)

        WIDTH = nwidth
        FIELD_WIDTH = WIDTH - 70

        #update the possitions of the buttons
        BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)

    #if the height changed
    if nheight != HEIGHT:

        HEIGHT = nheight

        #change the positions of the buttons
        BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)

    return WIDTH, HEIGHT, FIELD_WIDTH, BUTTON

#function to update the possitions of the buttons
def update_button_possitions(BUTTON, WIDTH, HEIGHT):

    #remove all buttons
    BUTTON = []

    #make all the buttons
    BUTTON.append(buttons(Text.FIELD_DEFAULT, (WIDTH - 50, 10), (40, 40), make.new_field, "default"))
    BUTTON.append(buttons(Text.FIELD_IF_STATEMENT, (WIDTH - 50, 60), (40, 40), make.new_field, "if"))
    BUTTON.append(buttons(Text.FIELD_WHILE_STATEMENT, (WIDTH - 50, 110), (40, 40), make.new_field, "while"))
    #BUTTON.append(buttons(theme.FIELD_FUNCTION, (WIDTH - 50, 160), (40, 40), make.new_field, "function"))
    BUTTON.append(buttons(Text.SAVE_AS_JSON, (WIDTH - 50, HEIGHT - 50), (40, 40), saveload.save_json, None))
    BUTTON.append(buttons(Text.SAVE_AS_IMAGE, (WIDTH - 50, HEIGHT - 100), (40, 40), saveload.save_image, None))
    BUTTON.append(buttons(Text.LOAD_JSON, (WIDTH - 50, HEIGHT - 150), (40, 40), saveload.load_json, None))
    BUTTON.append(buttons(Text.FIELD_DELETE, (60, HEIGHT - 50), (40, 40), edit.delete_field, None))
    BUTTON.append(buttons(Text.BACK, (10, HEIGHT - 50), (40, 40), edit.load_backup, None))

    return BUTTON

#function for changing the width of fields
def change_field_width(new_field_width, FIELDS, WIDTH):

    #making a library with all the fields sorted per y position
    lines = {}
    for field in FIELDS:
        if not field.rect.y in lines:
            lines[field.rect.y] = [[field.rect.x, field]]
        else:
            lines[field.rect.y].append([field.rect.x, field])

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

            print(old_x)
            print(field[1].rect)

            #changing the width of the field
            old_width = field[1].rect.width
            field[1].rect.width = field[1].rect.width * ((new_field_width / (WIDTH - 70)))

            #changing the x pos
            old_x_pos = field[1].rect.x
            try:

                #trying to load the x pos from already changed fields with the same x pos
                off = old_x[field[1].old_x]
                field[1].rect.x = off
                print(field[1].type)
                print(field[1].name)
                print(field[1].rect)

            #if the x possition hasn't been used already
            except:
                old = field[1].rect.x
                field[1].rect.x = field[1].rect.x + offset
                
                special = ["if-dan", "if-anders", "placeholder", "if-sec-F"]
                if field[1].type in special:
                    main = FIELDS[FIELDS.index(field[1]) - special.index(field[1].type) - 1]
                    if field[1].type in ["if-dan", "if-sec-T"]:
                        field[1].rect.x = main.rect.x + Window.MARGIN_IF_STATEMENT_LEFT
                    if field[1].type in ["if-dan", "if-anders"]:
                        field[1].rect.width = main.rect.width / 2 - 15
                    if field[1].type in ["if-anders"]:
                        field[1].rect.x = main.rect.x + main.rect.width/2 + 25
                    if field[1].type in ["if-sec-T", "if-sec-F"]:
                        field[1].rect.width = main.rect.width / 2 - Window.MARGIN_IF_STATEMENT_LEFT / 2 - Window.MARGIN_IF_STATEMENT_MIDDLE / 2
                    if field[1].type in ["if-sec-F"]:
                        pre = FIELDS[FIELDS.index(field[1]) - 1]
                        field[1].rect.x = pre.rect.x + pre.rect.width + Window.MARGIN_IF_STATEMENT_MIDDLE
                if field[1].type == "while-sec":
                    main = FIELDS[FIELDS.index(field[1]) - 1]
                    field[1].rect.x = main.rect.x + Window.MARGIN_WHILE_STATEMENT
                old_x[field[1].old_x] = field[1].rect.x
            
            if field[1].type == "if-anders":
                print(FIELDS[FIELDS.index(field[1]) - 2].type)
                field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 2].rect.x + FIELDS[FIELDS.index(field[1]) - 2].rect.width - field[1].rect.x
            elif field[1].type == "while-sec":
                print(FIELDS[FIELDS.index(field[1]) -1].type)
                field[1].rect.width = FIELDS[FIELDS.index(field[1]) - 1].rect.x + FIELDS[FIELDS.index(field[1]) - 1].rect.width - field[1].rect.x
            else:
                for place in adjusted:
                    if place.old_x == field[1].old_x and place.old_w == field[1].old_w:
                        field[1].rect.width = place.rect.width

                '''print(field[1].type)
                print(field[1].rect)
                print(field[1].name)
                print(field[1].old_x)'''
            adjusted.append(field[1])
            offset += field[1].rect.width + field[1].rect.x - old_width - old_x_pos
