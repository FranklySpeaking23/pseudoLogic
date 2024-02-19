#importing needed files
from Settings import Colors, Window, Patern
import pygame

#function to draw the side lines of a while-statement
def side_lines(surface, offset, start, FIELDS, WIDTH):

    #getting the height that all the fields together need
    hoogte = 0
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y

    hoogte = hoogte + 10

    for field in FIELDS:
        if (field.type == "while" and Window.SIDEBAR_WHILE_STATEMENT) or (field.type == "if" and Window.SIDEBAR_IF_STATEMENT):
            if field.type == "if":
                breedte = Window.WIDTH_SIDEBAR_IF_STATEMENT
                color = Colors.IF_STATEMENT
            else:
                breedte = Window.WIDTH_SIDEBAR_WHILE_STATEMENT
                color = Colors.WHILE_STATEMENT
            rect = pygame.Rect(field.rect.x, field.rect.y, breedte, Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT)
            run = True
            while run and rect.y < hoogte:
                cont = True
                for item in FIELDS:
                    if rect.colliderect(item) and item != field:
                        run = False
                        cont = False
                        break
                if not cont:
                    continue
                pygame.draw.rect(surface, color, pygame.Rect(rect.x, rect.y - offset, rect.width, rect.height + 5), Window.BORDER, Window.ROUNDING)
                rect.y += Window.MARGIN_HEIGHT + Window.FIELD_HEIGHT

    '''#iterating through the width of the screen
    for breedte in range(start, WIDTH - 50, Window.WIDTH_SIDEBAR_WHILE_STATEMENT):
        blocks = []

        #iterating through the height of the screen
        for i in range(10, repetition, Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT):

            #setting an initial rectangle
            rect = pygame.Rect(breedte, i - offset, Window.WIDTH_SIDEBAR_WHILE_STATEMENT, Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT + 10)

            #iterating through all the fields
            collision = False
            source = None
            for item in FIELDS:
                
                #making the field comparable
                comp_rect = pygame.Rect(item.rect.x, item.rect.y - offset, item.rect.width, item.rect.height)

                #checking collision
                if rect.colliderect(comp_rect):

                    #check collision with fields
                    if pygame.Rect(rect.x, rect.y, rect.width, Window.FIELD_HEIGHT).colliderect(comp_rect):
                        if (item.type == "while" and Window.SIDEBAR_WHILE_STATEMENT) or (item.type == "if" and Window.SIDEBAR_IF_STATEMENT):
                            pass
                        else:
                            collision = True
                    
                    if item.type in ["while", "if"]:
                        source = item
                    
            #if no collision with fields other than while-statements
            if not collision:

                #iterate through previous rects
                for block in blocks:

                    #if collision with a previous field (prevent drawing on empty space)
                    if block[0].colliderect(rect):

                        #align rect and draw to screen
                        rect = pygame.Rect(block[0].x, rect.y, rect.width, rect.height)
                        pygame.draw.rect(surface, block[1], rect, Window.BORDER, Window.ROUNDING)
                        blocks.append([rect, block[1]])
                        break

                
                else:
                    if source != None:
                        #if rect touches while-statement
                        if source.type == "while":
                            color = Colors.WHILE_STATEMENT
                        else:
                            color = Colors.IF_STATEMENT

                        #align rect with field and draw to screen
                        rect = pygame.Rect(source.rect.x, source.rect.y - offset, rect.width, rect.height)
                        pygame.draw.rect(surface, color, rect, Window.BORDER, Window.ROUNDING)
                        blocks.append([rect, color])'''

#function for drawing lines as the background of the application
def lines(surface, sort, WIDTH, HEIGHT):

    #checking what type of lines to draw and drawing them to the screen
    if sort == "fancy_lines":
        for i in range(0, WIDTH, 10):
            pygame.draw.line(surface, Patern.BACKGROUND_LINE_COLOR, (i, HEIGHT - i), (WIDTH - i, i))
    elif sort == "triangle_lines":
        for i in range(0, WIDTH, 10):
            pygame.draw.line(surface, Patern.BACKGROUND_LINE_COLOR, (i, HEIGHT), (WIDTH - i, 0))
    elif sort == "diagonal_lines":
        for i in range(0, WIDTH*2, 10):
            pygame.draw.line(surface, Patern.BACKGROUND_LINE_COLOR, (-1 * WIDTH + i, HEIGHT), (i, 0))
    elif sort == "no_lines":
        pass

#function for drawing the screen
def display(finale_surface, mouse, offset, time, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT):

    #making a temporary surface
    surface = pygame.Surface((finale_surface.get_width(), finale_surface.get_height()))
    
    #making the background
    surface.fill(Colors.BACKGROUND)
    lines(surface, Patern.BACKGROUND_PATERN, WIDTH, HEIGHT)

    #drawing the side lines (before the fields --> if an error appears, the fields are still on top)
    side_lines(surface, offset, 10 - Window.WIDTH_SIDEBAR_WHILE_STATEMENT, FIELDS, WIDTH)
    
    #drawing the fields and buttons
    for item in FIELDS:
        item.draw(surface, mouse, offset, time, selected_field)
    for item in FIELDS:
        if item.type == "if":
            item.draw(surface, mouse, offset, time, selected_field)

    for item in BUTTON:
        item.draw(surface, (mouse[0], mouse[1] - offset), 0, time, selected_field)

    #moving to the original surface
    finale_surface.blit(surface, (0, 0))

    #updating the display
    pygame.display.update()
