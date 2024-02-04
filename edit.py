from saveload import load_json
from Settings import Window

def load_backup(FIELDS, BACKUPS, WIDTH):
    if len(BACKUPS) > 0:
        temp = BACKUPS.pop(len(BACKUPS) - 1)
        FIELDS, WIDTH = load_json(temp, WIDTH, False)
    print("other fields:", FIELDS)
    print("loading backup")
    return FIELDS, BACKUPS

def delete_field(selected_field, FIELDS):
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
                '''for item in FIELDS:
                    if item != field and item.rect.colliderect(field.rect):
                        field.rect.y += theme.FIELD_HEIGHT + theme.MARGIN_HEIGHT
                        break'''
    selected_field = None
    return selected_field, FIELDS

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
