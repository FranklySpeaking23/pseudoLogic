#importing files
from dev import log, load_settings
import pygame
from saveload import load_json, save_json
from json import loads

SETTINGS = load_settings()

#function to restore program using a backup
def load_backup(FIELDS, BACKUPS, WIDTH):
    log("Loading backup", "func-s")
    if len(BACKUPS) > 0:
        temp = BACKUPS.pop(len(BACKUPS) - 1)
        FIELDS, WIDTH = load_json(temp, WIDTH, False)
    log("Loading backup", "func-e")
    return FIELDS, BACKUPS

'''def delete_field(selected_field, FIELDS):
    selec_x = selected_field.rect.x
    selec_w = selected_field.rect.width
    removed = 0
    selected_hoogte = selected_field.rect.y
    selected_breedte = selected_field.rect.x
    selected_width = selected_field.rect.width
    if selected_field.type == "while" or selected_field.type == "if":
        hoogte = selected_field.rect.y
        max_hoogte = selected_field.rect.y
        breedte = selected_field.rect.x
        fields_rm = [selected_field]
        groter = []
        alt_hoogte = selected_field.rect.y
        for field in FIELDS:
            if field.rect.y > hoogte and field.rect.x > breedte and field != selected_field:
                alt_hoogte = field.rect.y
            if field.rect.y > hoogte and field.rect.x <= breedte and field.rect.x + field.rect.width >= breedte + selected_width:
                groter.append(field.rect.y)
        try:
            hoogte = min(groter)
        except:
            hoogte = alt_hoogte + 1
        
        print(hoogte)
        for field in FIELDS:
            print(f"{field.name}:{field.type}:{field.rect}")
            if selected_field.rect.y <= field.rect.y < hoogte and breedte + selected_width > field.rect.x > breedte:
                print("Removed")
                fields_rm.append(field)
        removed = len(fields_rm)
        for field in fields_rm:
            FIELDS.remove(field)
    else:
        FIELDS.remove(selected_field)
        removed = 1

    print("moving")
    for i in range(1):
        print(i)
        for field in FIELDS:
            if field.rect.y > selected_hoogte and selec_x + selec_w > field.rect.x:
                print(f"{field.name}:{field.type}:{field.rect}")
                field.rect.y -= (Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT) * removed
    selected_field = None
    return selected_field, FIELDS'''

'''def delete_field(selected_field, FIELDS):
    hoogte = 0
    start_x = selected_field.rect.x
    breedte = selected_field.rect.width
    removed = 0
    if selected_field.type == "if":
        index = FIELDS.index(selected_field)
        FIELDS.pop(index + 2)
    for field in FIELDS:
        if selected_field.rect.x < field.rect.x < selected_field.rect.x + selected_field.rect.width:
            if field.rect.y > hoogte:
                hoogte = field.rect.y
    for field in FIELDS:
        if selected_field.rect.x < field.rect.x < selected_field.rect.x + selected_field.rect.width and selected_field.rect.y < field.rect.y <= hoogte:
            FIELDS.remove(field)
            removed += 1
    FIELDS.remove(selected_field)
    selected_field = None
    for field in FIELDS:
        if start_x < field.rect.x < start_x + breedte and field.rect.y > hoogte:
            field.rect.y -= removed * theme.FIELD_HEIGHT
            print(field.type, field.name, field.rect)
    return selected_field, FIELDS'''

'''def delete_field(selected_field, FIELDS):

    hoogte = selected_field.rect.y
    alt = selected_field.rect.y
    for item in field:
        if item.rect.x > selected_field.rect.x and item.rect.x + item.rect.width <= selected_field.rect.x + selected_field.rect.width:
            if item.rect.y > hoogte:
                hoogte = item.rect.y
        elif hoogte < '''

def delete_field(selected_field, FIELDS):
    from make import new_field
    log("Deleting fields", "func-s")
    fields = []
    fields.extend(FIELDS)
    fields.sort(key=lambda x:x.rect.y)

    con1 = None
    con2 = None
    for field in FIELDS:
        if field.rect.collidepoint((selected_field.rect.x, selected_field.rect.y - SETTINGS["field"]["height"] - SETTINGS["field"]["margin_height"] + 5)) and (field.type == "if" or field.type == "while"):
            print("if")
            con1 = "if"
        print((selected_field.rect.x, selected_field.rect.y + SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"] + 3))
        if field.rect.collidepoint((selected_field.rect.x, selected_field.rect.y + SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"] + 3)):
            print("block")
            con2 = "block"
            
    if (con1==None or con2=="block") or not selected_field.type in ["if-sec-T", "if-sec-F", "while-sec"]:# or (not selected_field.type in ["if-sec-T", "if-sec-F"]):
        print(1)
        removed_items = select_indent(FIELDS, selected_field)
        for item in removed_items:
            fields.remove(item)
            FIELDS.remove(item)

        removed = len (removed_items)

        for k in range(removed):
            for i, field in enumerate(fields):
                if field.rect.y > 20 and (not field.type in ["if-dan", "if-anders"]): 
                    new_height = field.rect.y - SETTINGS["field"]["margin_height"] - SETTINGS["field"]["height"]
                    for j in range(i):
                        item = fields[j]
                        if item.rect.collidepoint((field.rect.x, new_height)) or item.rect.collidepoint((field.rect.x, new_height + 10)):
                            if not ((field.type == "if-dan" or field.type == "if-anders") and item.type == "if"):
                                break
                    else:
                        checking = []
                        for j in range(i):
                            item = fields[j]
                            if item.rect.y + SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"] >= field.rect.y:
                                checking.append(item)
                        for item in checking:
                            if field.rect.x < item.rect.x < field.rect.x + field.rect.width:
                                if not ((field.type == "if-dan" or field.type == "if-anders") and item.type == "if"):
                                    break
                        else:
                            if field.type == "if":
                                FIELDS[FIELDS.index(field) + 1].rect.y = new_height + 10
                                FIELDS[FIELDS.index(field) + 2].rect.y = new_height + 5
                            field.rect.y = new_height
    if not (con1==None or con2=="block") and not selected_field.type in ["if-sec-F", "if-sec-T", "while-sec"]:
        print(2)
        selc = None
        for field in FIELDS:
            if selected_field.rect.collidepoint((field.rect.x + (selected_field.rect.x - field.rect.x), field.rect.y + SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"] + 5)) and field.type == "if":
                if field.rect.x + field.rect.width//2 - SETTINGS["field"]["margin_if_left"]//2 - SETTINGS["field"]["margin_if_middle"]//2 > selected_field.rect.x:
                    typ = "if-sec-T"
                else:
                    typ = "if-sec-F"
                selc = field
                print("check")
                break
            if selected_field.rect.collidepoint((field.rect.x + (selected_field.rect.x - field.rect.x), field.rect.y + SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"] + 5)) and field.type == "while":
                typ = "while-sec"
                selc = field
                print("check")
                break
        else:
            typ = "if-sec-F"
            selc = FIELDS[-1]
        print(selc.rect)
        FIELDS, temp = new_field(typ, FIELDS, field, None, shift=True)
        FIELDS[-1].show = False
    
    else:
        selected_field.show = False

    #FIELDS = fields
    selected_field = None
    log("Deleting fields", "func-e")
    return selected_field, FIELDS

def select_indent(FIELDS, selected_field):
    log("Selecting indent", "func-s")
    fields = []
    fields.extend(FIELDS)
    fields.sort(key=lambda x:x.rect.y)
    

    height = selected_field.rect.y
    max_height = None
    for field in fields:
        if field.rect.y > height:
            height = field.rect.y

        if field.rect.x <= selected_field.rect.x and field.rect.x + field.rect.width > selected_field.rect.x:
            if field.rect.y > selected_field.rect.y: 
                if max_height == None or field.rect.y < max_height:
                    max_height = field.rect.y

    if max_height == None:
        max_height = height + 10


    removed_items = [selected_field]
    for field in FIELDS:
        if selected_field.rect.x < field.rect.x < selected_field.rect.x + selected_field.rect.width and field.rect.x + field.rect.width <= selected_field.rect.x + selected_field.rect.width + 10:
            if selected_field.rect.y < field.rect.y < max_height:
                removed_items.append(field)

    log("Selecting indent", "func-e")
    return removed_items

def move_down(amount_added, height_added, FIELDS):
    log("Moving down", "func-s")
    fields = []
    fields.extend(FIELDS)
    fields = fields[0:len(FIELDS) - amount_added]
    fields.sort(key=lambda x:x.rect.y)
    if fields != None:
        for i in range(height_added):
            for item in fields:
                for r in FIELDS:
                    if item.rect.colliderect(r.rect) and r != item and (not item.type in ["if-dan", "if-anders"]):
                        if (item.type == "if" and (not r.type in ["if-dan", "if-anders"])) or item.type != "if":
                            if item.type == "if":
                                FIELDS[FIELDS.index(item) + 1].rect.y += SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"]
                                FIELDS[FIELDS.index(item) + 2].rect.y += SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"]

                            item.rect.y += SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"]
                            break
    log("Moving down", "func-e")

def copy(FIELDS, selected_field, saved):
    log("Copy", "func-s")

    if selected_field != None:
        fields = select_indent(FIELDS, selected_field)

        temp = selected_field.rect.x
        for field in fields:
            field.rect.x -= temp

        width = selected_field.rect.width
        saved = save_json(fields, width, False)

        for field in fields:
            field.rect.x += temp

    log("Copy", "func-e")
    return saved

def paste(FIELDS, selected_field, copy, WIDTH):
    log("Paste", "func-s")
    from resize import change_field_width

    if copy != None:
        fields, width = load_json(copy, selected_field.rect.width + 70, False, False)

        for field in fields:
            field.rect.x += selected_field.rect.x
        
        temp = fields[0].rect.y
        shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
        for field in fields:
            field.rect.y -= temp
            field.rect.y += selected_field.rect.y
            if not shift:
                field.rect.y += SETTINGS["field"]["height"] + SETTINGS["field"]["margin_height"]
        
        '''for field in fields:
            field.old_w = field.rect.width / (WIDTH / Window.WIDTH)
            field.old_x = field.rect.x '''

        log(f"{selected_field.rect.width}", "log")
        change_field_width(selected_field.rect.width, fields, width + 70)

        FIELDS.extend(fields)

        for field in FIELDS:
            field.old_w = field.rect.width
            field.old_x = field.rect.x

        y_pos = {}
        for field in fields:
            try:
                y_pos[field.rect.y].append(field)
            except:
                y_pos[field.rect.y] = [field]
        height_added = 0

        for pos in y_pos:
            if (not pos + 10 in y_pos) and (not pos + 5 in y_pos):
                height_added += 1
        move_down(len(fields), height_added, FIELDS)

    log("Paste", "func-e")
    return FIELDS

def check_prop(selected_field):
    if selected_field != None and "prop" in selected_field.name:
        try:
            prop = selected_field.name.split("prop")[1]
            prop = prop.split("}")[0] + "}"
            prop = loads(prop)
            if "type" in prop:
                name = prop["type"]
                if name in ["default", "if", "if-dan", "if-anders", "if-sec-T", "if-sec-F", "while", "while-sec"]:
                    selected_field.type = name
            if "rect" in prop:
                try:
                    selected_field.rect.x = prop["rect"][0]
                    selected_field.rect.y = prop["rect"][1]
                    selected_field.rect.width = prop["rect"][2]
                    selected_field.rect.height = prop["rect"][3]
                except:
                    pass
            if "old_x" in prop:
                selected_field.old_x = prop["old_x"]
            if "old_w" in prop:
                selected_field.old_w = prop["old_w"]
            if "show" in prop:
                selected_field.show = prop["show"]
            if "border" in prop:
                selected_field.border = prop["border"]

        except:
            pass
