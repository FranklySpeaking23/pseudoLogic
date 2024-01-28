from Settings import Colors, Window, Patern
import pygame

def side_lines(surface, offset, start, FIELDS, WIDTH):
    hoogte = 0
    for item in FIELDS:
        if item.rect.y > hoogte:
            hoogte = item.rect.y

    repetition = hoogte + 10
    for breedte in range(start, WIDTH - 50, Window.WIDTH_SIDEBAR_WHILE_STATEMENT):
        blocks = []
        for i in range(10, repetition, Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT):
            rect = pygame.Rect(breedte, i - offset, Window.WIDTH_SIDEBAR_WHILE_STATEMENT, Window.FIELD_HEIGHT + Window.MARGIN_HEIGHT + 10)
            collision = False
            source = None
            for item in FIELDS:
                comp_rect = pygame.Rect(item.rect.x, item.rect.y - offset, item.rect.width, item.rect.height)
                #pygame.draw.rect(surface, color, rect)
                if rect.collidepoint(comp_rect.topleft):
                    #rect = pygame.Rect(rect.x, rect.y, rect.width, theme.FIELD_HEIGHT)
                    if rect.collidepoint(comp_rect.topleft):
                        if item.type != "while" and pygame.Rect(rect.x, rect.y, rect.width, Window.FIELD_HEIGHT).collidepoint(comp_rect.topleft):
                            collision = True
                        if item.type == "while":
                            source = item
                    
            if not collision:
                if source != None:
                    rect = pygame.Rect(source.rect.x, rect.y, rect.width, rect.height)
                    pygame.draw.rect(surface, Colors.WHILE_STATEMENT, rect, Window.BORDER, Window.ROUNDING)
                    blocks.append(rect)
                else:
                    for block in blocks:
                        if block.colliderect(rect):
                            rect = pygame.Rect(block.x, rect.y, rect.width, rect.height)
                            pygame.draw.rect(surface, Colors.WHILE_STATEMENT, rect, Window.BORDER, Window.ROUNDING)
                            blocks.append(rect)
                            break

def lines(surface, sort, WIDTH, HEIGHT):
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

def display(finale_surface, mouse, offset, time, FIELDS, selected_field, BUTTON, WIDTH, HEIGHT):
    surface = pygame.Surface((finale_surface.get_width(), finale_surface.get_height()))
    surface.fill(Colors.BACKGROUND)
    lines(surface, Patern.BACKGROUND_PATERN, WIDTH, HEIGHT)
    #side_lines(surface, offset, theme.WIDTH_SIDEBAR_WHILE_STATEMENT, (200, 200, 200))
    side_lines(surface, offset, 10 - Window.WIDTH_SIDEBAR_WHILE_STATEMENT, FIELDS, WIDTH)
    
    counting = 0
    for item in FIELDS:
        item.draw(surface, mouse, offset, time, selected_field)
        counting += 1
    for item in BUTTON:
        item.draw(surface, (mouse[0], mouse[1] - offset), 0, time, selected_field)

    finale_surface.blit(surface, (0, 0))
    pygame.display.update()