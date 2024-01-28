from design import field
from Settings import Window, Text
import pygame

def new_field(type, FIELDS, selected_field, FIELD_WIDTH):
    amount_added = 0
    height_added = 0
    old_x = 0
    old_w = 0
    shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
    try:
        if (selected_field.type == "while" or selected_field.type == "if") and not shift:
            hoogte = selected_field.rect.y
            breedte = selected_field.rect.x
            for item in FIELDS:
                if item.rect.y > hoogte and item.rect.x > breedte:
                    hoogte = item.rect.y
            hoogte += Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT
            start_pos = (breedte, hoogte)
            pass_type = type
        else:
            start_pos = (selected_field.rect.topleft[0], selected_field.rect.topleft[1] + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)
        
            if type == "default":
                pass_type = selected_field.type
            else:
                pass_type = type
        dimensions = (selected_field.rect.width, selected_field.rect.height)
        old_x = selected_field.old_x
        old_w = selected_field.old_w
        if shift:
            start_pos = (start_pos[0], start_pos[1] - Window.FIELD_HEIGHT - Window.MARGIN_HEIGHT)
    except:
        hoogte = 10
        for veld in FIELDS:
            if veld.rect.y + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT > hoogte:
                hoogte = veld.rect.y + Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT
        start_pos = (10, hoogte)
        dimensions = (FIELD_WIDTH, Window.FIELD_HEIGHT)
        old_x = 10
        old_w = FIELD_WIDTH
        pass_type = type

    if shift:
        pass_type = type

    if selected_field != None:
        print(f"selected: {selected_field.type} : {selected_field.rect}")
    print(f"start_pos: {start_pos}")

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
        
        amount_added = 3
        height_added = 2

    '''elif type == "function":
        FIELDS.append(field(theme.FUNCTION_TEXT, start_pos, (dimensions[0], theme.FIELD_HEIGHT), type, 0, True, pygame.font.SysFont(theme.FIELDS_FONT, theme.FUNCTION_FONT_SIZE)))
        FIELDS.append(field(theme.FUNCTION_LOWER_TEXT, (start_pos[0] + 15, start_pos[0] + theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT), (dimensions[0] - 30, dimensions[1]), "function-sec"))'''


    if selected_field != None:
        for i in range(len(FIELDS) - amount_added):
            item = FIELDS[i]
            if item.rect.y >= start_pos[1]:
                print(item.name, ":", item.type, ":", item.rect)
                touch = False
                if (start_pos[0] + dimensions[0] >= item.rect.x >= start_pos[0] or item.rect.x < start_pos[0] < item.rect.x + item.rect.width) and (item != selected_field or shift):
                    touch = True
                if touch:
                    item.rect.y += (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT) * height_added
                    print(item.name, ":", item.type, ":", item.rect)
                print("_____________________")

        selected_field = FIELDS[len(FIELDS) - 1]

    return FIELDS, selected_field
