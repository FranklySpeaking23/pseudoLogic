#importing needed files / libraries
import pygame
from Settings import Window
#import update_checker
import draw
from resize import window_size, update_button_possitions
import edit

#initializing the window
WIDTH, HEIGHT = Window.WIDTH, Window.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(Window.TITLE)
FPS = Window.FPS
pygame.font.init()

#making variables
FIELDS = []
BUTTON = []
FIELD_WIDTH = WIDTH - 70



def main():

    #setting variables
    global selected_field, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS
    
    selected_field = None
    offset = 0

    BUTTON = update_button_possitions(BUTTON, WIDTH, HEIGHT)
    BACKUPS = []

    active_time = 0
    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)
        active_time += 1

        #checking if the window width changed (once every second)
        if active_time % FPS == 0:
            WIDTH, HEIGHT, FIELD_WIDTH, BUTTON = window_size(WIN, WIDTH, HEIGHT, FIELD_WIDTH, BUTTON, FIELDS)

        #setting the mouse possition (relative to window and offset)
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0], mouse[1] + offset)


        #looping through events
        for event in pygame.event.get():

            #checking for closing of program
            if event.type == pygame.QUIT:
                run = False

            #handeling mouse input
            if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):

                #checkiing button press
                for item in BUTTON:
                    FIELDS, selected_field, BACKUPS = item.execute((mouse[0], mouse[1] - offset), FIELDS, selected_field, FIELD_WIDTH, WIDTH, HEIGHT, BUTTON, BACKUPS)

                selected_field = None

                #checking field press
                for button in FIELDS:
                    selected_field = button.execute(mouse, selected_field)

            #inputting text in fields
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DELETE and selected_field != None:
                   selected_field, FIELDS = edit.delete_field(selected_field, FIELDS)

                elif selected_field != None:
                    selected_field = selected_field.typ(event, selected_field)

            #changing vertical offset
            if event.type == pygame.MOUSEWHEEL:
                offset -= event.y * Window.CHANGE_Y_POS
            
        #shorten the lenght of the backups
        if len(BACKUPS) > 10:
            BACKUPS.pop(0)

        #update the display
        draw.display(WIN, mouse, offset, active_time, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT)

    #quit the program
    pygame.quit()


#run the program
if __name__ == "__main__":
    main()
