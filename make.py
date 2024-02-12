#importing needed files
from design import field
from Settings import Window, Text
import pygame

#function for making a new field
def new_field(type, FIELDS, selected_field, FIELD_WIDTH):

    #making some variables
    amount_added = 0
    height_added = 0
    old_x = 0
    old_w = 0
    shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]

    try:

        #if the current field is an if- or while-statement and the field needs to be below the current field
        if (selected_field.type == "while" or selected_field.type == "if") and not shift:

            #getting the height of statement
            hoogte = selected_field.rect.y
            breedte = selected_field.rect.x
            for item in FIELDS:
                if item.rect.y > hoogte and item.rect.x > breedte:
                    hoogte = item.rect.y
            hoogte += Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT

            #setting a start possition and type for new fields
            start_pos = (breedte, hoogte)
            pass_type = type

        else:

            #setting a start possition and type for new fields
            start_pos = (selected_field.rect.topleft[0], selected_field.rect.topleft[1] + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)
        
            if type == "default":
                pass_type = selected_field.type
            else:
                pass_type = type

        #setting a dimension for new fields
        dimensions = (selected_field.rect.width, selected_field.rect.height)


        old_x = selected_field.old_x
        old_w = selected_field.old_w

        #changing the start position if the field needs to be above the selected field
        if shift:
            start_pos = (start_pos[0], start_pos[1] - Window.FIELD_HEIGHT - Window.MARGIN_HEIGHT)

    #if an error appears (e.g. there is no selected field)
    except:

        #setting the new field height
        hoogte = 10
        for veld in FIELDS:
            if veld.rect.y + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT > hoogte:
                hoogte = veld.rect.y + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT

        #setting a start possition and dimensions for the new fields
        start_pos = (10, hoogte)
        dimensions = (FIELD_WIDTH, Window.FIELD_HEIGHT)

        old_x = 10
        old_w = FIELD_WIDTH
        pass_type = type

    if shift:
        pass_type = type

    #making the new field(s) based on the type of the field(s)
    if type == "default":
        FIELDS.append(field(Text.DEFAULT_TEXT, start_pos, (dimensions[0], Window.FIELD_HEIGHT), pass_type, old_x, old_w))
        amount_added = 1
        height_added = 1
    elif type == "if":
        FIELDS.append(field(Text.IF_STATEMENT_TEXT, start_pos, (dimensions[0], Window.FIELD_HEIGHT), pass_type, old_x, old_w)),
        FIELDS.append(field(Text.IF_STATEMENT_LEFT, (start_pos[0] + Window.MARGIN_IF_STATEMENT_LEFT, start_pos[1] + 10), (dimensions[0] / 2 - 15, Window.FIELD_HEIGHT - 10), "if-dan", old_x + Window.MARGIN_IF_STATEMENT_LEFT, old_w / 2 - 15))
        FIELDS.append(field(Text.IF_STATEMENT_RIGHT, (start_pos[0] + dimensions[0] // 2 + Window.MARGIN_IF_STATEMENT_LEFT/2 + Window.MARGIN_IF_STATEMENT_MIDDLE/2, start_pos[1] + 5), (dimensions[0] / 2 - 15, Window.FIELD_HEIGHT - 5), "if-anders", old_x + old_w // 2 + 25, old_w / 2 - 15))
        FIELDS.append(field(Text.IF_STATEMENT_B_LEFT, (start_pos[0] + Window.MARGIN_IF_STATEMENT_LEFT, start_pos[1] + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT), (dimensions[0] / 2 - Window.MARGIN_IF_STATEMENT_LEFT/2 - Window.MARGIN_IF_STATEMENT_MIDDLE/2, Window.FIELD_HEIGHT), "if-sec-T", old_x + Window.MARGIN_IF_STATEMENT_LEFT, old_w / 2 - Window.MARGIN_IF_STATEMENT_LEFT/2 - Window.MARGIN_IF_STATEMENT_MIDDLE/2))
        FIELDS.append(field(Text.IF_STATEMENT_B_RIGHT, (start_pos[0] + dimensions[0] // 2 + Window.MARGIN_IF_STATEMENT_LEFT/2 + Window.MARGIN_IF_STATEMENT_MIDDLE/2, start_pos[1] + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT), (dimensions[0] / 2 - Window.MARGIN_IF_STATEMENT_MIDDLE/2 - Window.MARGIN_IF_STATEMENT_LEFT/2, Window.FIELD_HEIGHT), "if-sec-F", old_x + old_w // 2 + Window.MARGIN_IF_STATEMENT_LEFT/2 + Window.MARGIN_IF_STATEMENT_MIDDLE/2, old_w / 2 - Window.MARGIN_IF_STATEMENT_MIDDLE/2 - Window.MARGIN_IF_STATEMENT_LEFT/2))
        amount_added = 5
        height_added = 2
    elif type == "while":
        FIELDS.append(field(Text.WHILE_STATEMENT_TEXT, start_pos, (dimensions[0], Window.FIELD_HEIGHT), type, old_x, old_w)),
        FIELDS.append(field(Text.WHILE_STATEMENT_LOWER_TEXT, (start_pos[0] + Window.MARGIN_WHILE_STATEMENT, start_pos[1] + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT), (dimensions[0] - Window.MARGIN_WHILE_STATEMENT, Window.FIELD_HEIGHT), "while-sec", old_x + Window.MARGIN_WHILE_STATEMENT, old_w - Window.MARGIN_WHILE_STATEMENT))
        
        amount_added = 2
        height_added = 2

    '''elif type == "function":
        FIELDS.append(field(theme.FUNCTION_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), type, 0, True, pygame.font.SysFont(theme.FIELDS_FONT, theme.FUNCTION_FONT_SIZE)))
        FIELDS.append(field(theme.FUNCTION_LOWER_TEXT, (start_pos[0] + 15, start_pos[0] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] - 30, dimensions[1]), "function-sec"))'''


    #moving the other fields
    
    print("_" * 50)
    fields = []
    fields.extend(FIELDS)
    fields = fields[0:len(FIELDS) - amount_added]
    fields.sort(key=lambda x:x.rect.y)
    print(fields)
    if fields != None:
        print("fjeosj")
        for item in fields:
            for r in FIELDS:
                print(f"{item.type} : {item.rect} --- {r.type} : {r.rect}")
                if item.rect.colliderect(r.rect) and r != item and (not item.type in ["if-dan", "if-anders"]):
                    if (item.type == "if" and (not r.type in ["if-dan", "if-anders"])) or item.type != "if":
                        if item.type == "if":
                            FIELDS[FIELDS.index(item) + 1].rect.y += height_added * (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)
                            FIELDS[FIELDS.index(item) + 2].rect.y += height_added * (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)

                        print(item.rect, ":", r.rect)
                        item.rect.y += height_added * (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)
                        break


    '''if selected_field != None:

        #iterate through all other fields than the newly added onces
        for i in range(len(FIELDS) - amount_added):
            item = FIELDS[i]

            #if the y position is greater than the y possition of the new fields
            if item.rect.y >= start_pos[1]:
                print(item.name, ":", item.type, ":", item.rect)

                #checking the width and changing the height
                if (start_pos[0] + dimensions[0] >= item.rect.x >= start_pos[0] or item.rect.x < start_pos[0] < item.rect.x + item.rect.width) and (item != selected_field or shift):
                    item.rect.y += (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT) * height_added
                    print(item.name, ":", item.type, ":", item.rect)
                print("_____________________")
                
        #setting the selected field to the one that is last added
        selected_field = FIELDS[len(FIELDS) - 1]'''

    return FIELDS, selected_field
