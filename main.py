import pygame
from Settings import Window, Text
import update_checker
import draw
from resize import window_size, update_button_possitions
import edit

WIDTH, HEIGHT = Window.WIDTH, Window.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(Window.TITLE)
FPS = Window.FPS
pygame.font.init()

BUTTON_FONT = pygame.font.SysFont(Text.BUTTONS_FONT, Text.BUTTONS_FONT_SIZE)
TEXT_FONT = pygame.font.SysFont(Text.FIELDS_FONT, Text.FIELDS_FONT_SIZE)

FIELDS = []
BUTTON = []
FIELD_WIDTH = WIDTH - 70



def main():
    global selected_field
    global WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS
    active_time = 0
    run = True
    clock = pygame.time.Clock()
    selected_field = None
    offset = 0
    BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)
    BACKUPS = []

    while run:
        clock.tick(FPS)
        active_time += 1
        if active_time % FPS == 0:
            WIDTH, HEIGHT, FIELD_WIDTH, BUTTON = window_size(WIN, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS)
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0], mouse[1] + offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in BUTTON:
                    FIELDS, selected_field, BACKUPS = item.execute((mouse[0], mouse[1] - offset), FIELDS, selected_field, FIELD_WIDTH, WIDTH, HEIGHT, BUTTON, BACKUPS)
                selected_field = None
                for button in FIELDS:
                    selected_field = button.execute(mouse, selected_field)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE and selected_field != None:
                   selected_field, FIELDS = edit.delete_field(selected_field, FIELDS)
                if selected_field != None:
                    selected_field = selected_field.typ(event, selected_field)

            if event.type == pygame.MOUSEWHEEL:
                offset -= event.y * Window.CHANGE_Y_POS
            
            if len(BACKUPS) > 10:
                BACKUPS.pop(0)
        draw.display(WIN, mouse, offset, active_time, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)

    pygame.quit()


if __name__ == "__main__":
    main()
