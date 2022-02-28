import pygame
import sys
from module import *

pygame.font.init()
width = 1200
height = 675
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("CityWars")

# Text displayed on game
roboto = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf',20)
roboto_small = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf',14)
text_exit = roboto.render('Exit' , True, (255,255,255))
text_r = roboto.render('Red', True, (255,255,255))
text_g = roboto.render('Green', True, (255,255,255))
text_b = roboto.render('Blue', True, (255,255,255))

# Funciton that draws the menu at top right of the screen (rectangles + text)
def draw_top_menu(win, mouse):
    # Rectangles
    pygame.draw.rect(win,(20, 20, 20),[width-100,0,100,25])
    pygame.draw.rect(win,(20, 20, 20),[width-200,0,100,25])
    pygame.draw.rect(win,(20, 20, 20),[width-300,0,100,25])
    pygame.draw.rect(win,(20, 20, 20),[width-400,0,100,25])

    # Highlight hovered
    if width-100 <= mouse[0] <= width and 0 <= mouse[1] <= 25:
        pygame.draw.rect(win,(50, 50, 50),[width-100,0,100,25])
    elif width-200 <= mouse[0] <= width-100 and 0 <= mouse[1] <= 25:
        pygame.draw.rect(win,(50, 50, 50),[width-200,0,100,25])
    elif width-300 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 25:
        pygame.draw.rect(win,(50, 50, 50),[width-300,0,100,25])
    elif width-400 <= mouse[0] <= width-300 and 0 <= mouse[1] <= 25:
        pygame.draw.rect(win,(50, 50, 50),[width-400,0,100,25])

    # Text
    win.blit(text_exit, (width-65,0))
    win.blit(text_r, (width-160,0))
    win.blit(text_g, (width-270,0))
    win.blit(text_b, (width-365,0))

# Draws bottom menu in city view -------            (text needs to be added)
def draw_bottom_menu(win, mouse, c):
    pygame.draw.rect(win, (0,0,0), [width/2-300-2,height-100-2,604,54], 2)      # Border
    pygame.draw.rect(win,c,[width/2-300,height-100,150,50])                     # Rectangles
    pygame.draw.rect(win,c,[width/2-150,height-100,150,50])
    pygame.draw.rect(win,c,[width/2,height-100,150,50])
    pygame.draw.rect(win,c,[width/2+150,height-100,150,50])
    c2 = tuple([color + 50 if color < 205 else color for color in c])       # Change color for highlighted option

    # Highlight hovered
    if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:
        pygame.draw.rect(win,c2,[width/2-300,height-100,150,50])
    elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:
        pygame.draw.rect(win,c2,[width/2-150,height-100,150,50])
    elif width/2 <= mouse[0] <= width/2+150 and height-100 <= mouse[1] <= height-50:
        pygame.draw.rect(win,c2,[width/2,height-100,150,50])
    elif width/2+150 <= mouse[0] <= width/2+300 and height-100 <= mouse[1] <= height-50:
        pygame.draw.rect(win,c2,[width/2+150,height-100,150,50])

# Draws map movement buttons ------                 (text needs to be added)
def draw_map_move_buttons(win, mouse):
    # Rectangles
    pygame.draw.rect(win,(100,100,255),[width-150,height-202,50,50])     # Up arrow rect
    pygame.draw.rect(win,(100,100,255),[width-150,height-98,50,50])     # Down arrow rect
    pygame.draw.rect(win,(100,100,255),[width-202,height-150,50,50])     # Left arrow tect
    pygame.draw.rect(win,(100,100,255),[width-98,height-150,50,50])     # Right arrow rect

    # Hovered
    if width-150 <= mouse[0] <= width-100 and height-202 <= mouse[1] <= height-152:
        pygame.draw.rect(win,(150,150,255),[width-150,height-202,50,50])     # Up arrow rect
    elif width-150 <= mouse[0] <= width-100 and height-98 <= mouse[1] <= height-48:    
        pygame.draw.rect(win,(150,150,255),[width-150,height-98,50,50])     # Down arrow rect
    elif width-202 <= mouse[0] <= width-152 and height-150 <= mouse[1] <= height-100:
        pygame.draw.rect(win,(150,150,255),[width-202,height-150,50,50])     # Left arrow tect
    elif width-98 <= mouse[0] <= width-48 and height-150 <= mouse[1] <= height-100:
        pygame.draw.rect(win,(150,150,255),[width-98,height-150,50,50])     # Right arrow rect

    # Borders 
    pygame.draw.rect(win,(0,0,0),[width-152,height-204,54,54],2)     # Up arrow rect
    pygame.draw.rect(win,(0,0,0),[width-152,height-100,54,54],2)     # Down arrow rect
    pygame.draw.rect(win,(0,0,0),[width-204,height-152,54,54],2)     # Left arrow tect
    pygame.draw.rect(win,(0,0,0),[width-100,height-152,54,54],2)     # Right arrow rect

    # Draws city (just building outlines for now)
def draw_city(win, mouse, size):
    pygame.draw.rect(win,(255,255,255),[width/2-352,height/2-282,704,504], 2)       # Border
    #pygame.draw.rect(win,(255,255,255),[width/2-302,height/2-257,604,454], 2)       # Temp: just to see outlines
    if size == 6:
        # Building slot outlines
        pygame.draw.rect(win,(50,200,50),[width/2-225,height/2-180,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-75,height/2-180,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+75,height/2-180,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-225,height/2-30,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-75,height/2-30,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+75,height/2-30,150,150], 2)
    elif size == 9:
        # Building slot outlines
        pygame.draw.rect(win,(50,200,50),[width/2-225,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-75,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+75,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-225,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-75,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+75,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-225,height/2+45,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-75,height/2+45,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+75,height/2+45,150,150], 2)
    elif size == 12:
        # Building slot outlines
        pygame.draw.rect(win,(50,200,50),[width/2-300,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-150,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+150,height/2-255,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-300,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-150,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+150,height/2-105,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-300,height/2+45,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2-150,height/2+45,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2,height/2+45,150,150], 2)
        pygame.draw.rect(win,(50,200,50),[width/2+150,height/2+45,150,150], 2)

def draw_tasks(win, mouse, c_tasks=[], o_tasks=[]):
    pygame.draw.rect(win,(255,255,255),[23,55,204,504], 2)          # Border
    text_current = roboto.render("Current:", True, (0, 0, 0))
    win.blit(text_current, (28, 60))                                # Prints "Current:" on top of task box
    offset = 25
    #Current tasks
    for task in c_tasks:
        h=offset
        string = str(task)
        for line in string.split("\n"):
            temp = roboto_small.render(line, True, (0,0,0))
            win.blit(temp, (30, 60 + offset))                                   # Task text
            offset += 20
        offset += 10
        pygame.draw.rect(win, (20, 20, 20), [28,55+h, 194, offset-h-2], 2)     # Task border
    text_ongoing = roboto.render("Ongoing:", True, (0, 0, 0))
    win.blit(text_ongoing, (28, 60 + offset))
    offset += 25
    #Ongoing tasks
    for task in o_tasks:
        h=offset
        string = str(task)
        for line in string.split("\n"):
            temp = roboto_small.render(line, True, (0,0,0))
            win.blit(temp, (30, 60 + offset))                                   # Task text
            offset += 20
        offset += 10
        pygame.draw.rect(win, (20, 20, 20), [28,55+h, 194, offset-h-2], 2)     # Task border




# Updates display (GUI)
def redraw_window(win, view, mouse):
    if view == 1: 
        win.fill((255,0,0))
        draw_bottom_menu(win, mouse, (255, 100, 100))
    elif view == 2:
        win.fill((0,255,0))
        draw_city(win, mouse, 6)
        draw_tasks(win, mouse, tasks, tasks2)
        draw_bottom_menu(win, mouse, (100, 255, 100))
    else:
        win.fill((0,0,255))
        draw_map_move_buttons(win, mouse)
        draw_bottom_menu(win, mouse, (100, 100, 255))
    draw_top_menu(win, mouse)
    pygame.display.update()


# Main function
def main():
    run = True
    clock = pygame.time.Clock()
    view = 1

    while run:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        redraw_window(win, view, mouse)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width-100 <= mouse[0] <= width and 0 <= mouse[1] <= 25:
                    run = False
                    pygame.quit()
                elif width-200 <= mouse[0] <= width-100 and 0 <= mouse[1] <= 25:
                    view = 1
                elif width-300 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 25:
                    view = 2
                elif width-400 <= mouse[0] <= width-300 and 0 <= mouse[1] <= 25:
                    view = 3

world1 = World(["Babnik", "NPC"])
ca = world1.spawn_city("Babnik", 6)
cd = world1.spawn_city("NPC", 6)
tasks = [Task(type="Build", data=["Iron Mine", 2], end_turn=3), Task(type="Upgrade",data=["Iron Mine"], end_turn=5), Task(type="Train", data=["Spy", 5], end_turn=7)]
tasks2 = [Task(type="Build", data=["Iron Mine", 2], end_turn=3), Task(type="Upgrade",data=["Iron Mine"], end_turn=5), Task(type="Train",data=["Spy", 5], end_turn=7), Task(type="Move Troops", data=[Army([10, 10, 0, 0, 0]), world1.map[ca], world1.map[cd], "Attack"], end_turn=9)]







main()
