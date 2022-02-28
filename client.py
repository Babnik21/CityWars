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
text_r = roboto.render('Reports', True, (255,255,255))
text_g = roboto.render('City', True, (255,255,255))
text_b = roboto.render('Map', True, (255,255,255))

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
    win.blit(text_r, (width-185,0))
    win.blit(text_g, (width-270,0))
    win.blit(text_b, (width-370,0))

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
    if size == 6:
        x, y = (3, 2)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-225+i*150,height/2-180+j*150,150,150], 2)
                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-180+j*150 <= mouse[1] <= height/2-30+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-225+i*150,height/2-180+j*150,150,150], 2)
    elif size == 9:
        x, y = (3, 3)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-225+i*150,height/2-255+j*150,150,150], 2)
                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-225+i*150,height/2-255+j*150,150,150], 2)
    elif size == 12:
        x, y = (4, 3)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-300+i*150,height/2-255+j*150,150,150], 2)
                if width/2-300+i*150 <= mouse[0] <= width/2-150+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-300+i*150,height/2-255+j*150,150,150], 2)

    # Draws tasks
def draw_tasks(win, mouse, c_tasks=[], o_tasks=[]):
    pygame.draw.rect(win,(255,255,255),[23,55,204,504], 2)          # Border
    text_current = roboto.render("Current:", True, (0, 0, 0))
    win.blit(text_current, (28, 58))                                # Prints "Current:" on top of task box
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
    win.blit(text_ongoing, (28, 58 + offset))
    offset += 25
    #Ongoing tasks
    for i in range(len(o_tasks)):
        h=offset
        string = str(o_tasks[i])
        if offset + 10 + 20 * len(string.split("\n")) > 500:
            temp = roboto.render(f"Unshown tasks: {len(o_tasks)-i}", True, (0,0,0))
            win.blit(temp, (30, 535))                                           # "x more tasks" text
            break 
        for line in string.split("\n"):
            temp = roboto_small.render(line, True, (0,0,0))
            win.blit(temp, (30, 60 + offset))                                   # Task text
            offset += 20
        offset += 10
        pygame.draw.rect(win, (20, 20, 20), [28,55+h, 194, offset-h-2], 2)      # Task border


def draw_reports(win, mouse, reports=[]):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    offset = 0
    for i in range(len(reports)):
        temp = str(reports[i]).split(".")
        pygame.draw.rect(win,(0,0,0),[width/2-347,height/2-277+offset,694,50], 2)       # Report border
        if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+offset <= mouse[1] <= height/2-227+offset:
            pygame.draw.rect(win,(212,175,55),[width/2-347,height/2-277+offset,694,50], 2)
        text_report = roboto.render(temp[0], True, (0,0,0))
        win.blit(text_report, (width/2-340,height/2-258+offset))                        # Report header
        offset += 52
        if offset >= 460:
            text_extra = roboto.render(f"Unshown reports: {len(reports)-i}", True, (0,0,0))
            win.blit(text_extra, (width/2-85, 530))                                     # "x more tasks" text
            break


# Updates display (GUI)
def redraw_window(win, view, mouse):
    if view == 1: 
        win.fill((255,0,0))
        draw_reports(win, mouse, reports=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        draw_bottom_menu(win, mouse, (255, 100, 100))
    elif view == 2:
        win.fill((0,255,0))
        draw_city(win, mouse, 12)
        draw_tasks(win, mouse)
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


tasks = [Task(type="Build", data=["Iron Mine", 2], end_turn=3), Task(type="Upgrade",data=["Iron Mine"], end_turn=2), Task(type="Train", data=["Spy", 5], end_turn=7)]
tasks2 = [Task(type="Build", data=["Iron Mine", 2], end_turn=3),Task(type="Upgrade",data=["Iron Mine"], end_turn=2), Task(type="Train",data=["Spy", 5], end_turn=7), Task(type="Move Troops", data=[Army([10, 10, 0, 0, 0]), world1.map[ca], world1.map[cd], "Attack"], end_turn=9)]






main()
