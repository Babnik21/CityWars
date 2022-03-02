from pickletools import markobject
import pygame
import sys
from module import *
from values import *

pygame.font.init()
width = 1200
height = 675
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("CityWars")

# Text displayed on game
roboto = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf',20)
roboto_small = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf',14)
pacifico = pygame.font.Font('fonts/Pacifico.ttf', 30)
pacifico_small = pygame.font.Font('fonts/Pacifico.ttf', 23)
pacifico_huge = pygame.font.Font('fonts/Pacifico.ttf', 70)

    # Draws next turn button in bottom left of the screen
def draw_next_turn_button(win, mouse, c):
    c2 = tuple([color + 50 if color < 205 else 255 for color in c])
    pygame.draw.rect(win,c,[23,580,204,50])
    if 23 <= mouse[0] <= 227 and 580 <= mouse[1] <= 630:
        pygame.draw.rect(win,c2,[23,580,204,50])
    pygame.draw.rect(win,(255,255,255),[23,580,204,50], 2)

    txt = pacifico.render("Next Turn", True, (0,0,0))
    win.blit(txt, (55, 575))

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
    text_exit = roboto.render('Exit' , True, (255,255,255))
    text_r = roboto.render('Reports', True, (255,255,255))
    text_g = roboto.render('City', True, (255,255,255))
    text_b = roboto.render('Map', True, (255,255,255))
    win.blit(text_exit, (width-65,0))
    win.blit(text_r, (width-185,0))
    win.blit(text_g, (width-270,0))
    win.blit(text_b, (width-370,0))

# Draws bottom menu in city view
def draw_bottom_menu(win, mouse, c):
    pygame.draw.rect(win, (0,0,0), [width/2-300-2,height-100-2,604,54], 2)      # Border
    pygame.draw.rect(win,c,[width/2-300,height-100,150,50])                     # Rectangles
    pygame.draw.rect(win,c,[width/2-150,height-100,150,50])
    pygame.draw.rect(win,c,[width/2,height-100,150,50])
    pygame.draw.rect(win,c,[width/2+150,height-100,150,50])
    c2 = tuple([color + 50 if color < 205 else 255 for color in c])       # Change color for highlighted option

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

    # Draws resource display
def draw_res(win, city):
    pygame.draw.rect(win,(255,255,255),[width-227,55,204,110], 2)          # Border
    food = roboto.render(f"Food: {city.resources[0]}/{200+values.warehouse_capacity[city.find_level('Warehouse')]}", True, (0,0,0))
    iron = roboto.render(f"Iron: {city.resources[1]}/{200+values.warehouse_capacity[city.find_level('Warehouse')]}", True, (0,0,0))
    gold = roboto.render(f"Gold: {city.resources[2]}/{10+values.bank_capacity[city.find_level('Bank')]}", True, (0,0,0))
    housing = roboto.render(f"Housing: {city.army.count()}/{75+values.housing_capacity[city.find_level('Housing')]}", True, (0,0,0))
    win.blit(food, (width-210, 60))
    win.blit(iron, (width-210, 85))
    win.blit(gold, (width-210, 110))
    win.blit(housing, (width-210, 135))

    # Draws city (just building outlines for now)
def draw_city(win, mouse, city):
    pygame.draw.rect(win,(255,255,255),[width/2-352,height/2-282,704,504], 2)       # Border
    wall_text = pacifico_small.render(f"Wall level {city.find_level('Wall')}", True, (0,0,0))
    win.blit(wall_text, (width/2-70, 520))
    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:     # Wall
        pygame.draw.rect(win, (255, 250, 205), [width/2-300, height/2+195, 600, 25], 2)
    if city.size == 6:
        x, y = (3, 2)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-225+i*150,height/2-180+j*150,150,150], 2)
                buil = pacifico.render(city.buildings[3*j + i + 1].type, True, (0,0,0))
                win.blit(buil, (width/2-225+i*150, height/2-145+j*150))
                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-180+j*150 <= mouse[1] <= height/2-30+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-225+i*150,height/2-180+j*150,150,150], 2)
    elif city.size == 9:
        x, y = (3, 3)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-225+i*150,height/2-255+j*150,150,150], 2)
                buil = pacifico.render(city.buildings[3*j + i + 1].type, True, (0,0,0))
                win.blit(buil, (width/2-225+i*150, height/2-220+j*150))
                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-225+i*150,height/2-255+j*150,150,150], 2)
    elif city.size == 12:
        x, y = (4, 3)
        for i in range(x):
            for j in range(y):
                pygame.draw.rect(win,(50,200,50),[width/2-300+i*150,height/2-255+j*150,150,150], 2)
                buil = pacifico.render(city.buildings[4*j + i + 1].type, True, (0,0,0))
                win.blit(buil, (width/2-300+i*150, height/2-220+j*150))
                if width/2-300+i*150 <= mouse[0] <= width/2-150+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                    pygame.draw.rect(win,(255,250,205),[width/2-300+i*150,height/2-255+j*150,150,150], 2)

    # Draws tasks
def draw_tasks(win, mouse, city):
    c_tasks, o_tasks = city.current_tasks, city.ongoing_tasks
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

    # Draws reports
def draw_reports(win, mouse, city):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    offset = 0
    for i in range(len(city.reports)):
        temp = str(city.reports[i]).split(".")
        pygame.draw.rect(win,(0,0,0),[width/2-347,height/2-277+offset,694,50], 2)       # Report border
        if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+offset <= mouse[1] <= height/2-227+offset:
            pygame.draw.rect(win,(212,175,55),[width/2-347,height/2-277+offset,694,50], 2)
        text_report = roboto.render(temp[0], True, (0,0,0))
        win.blit(text_report, (width/2-340,height/2-265+offset))                        # Report header
        offset += 52
        if offset >= 460:
            text_extra = roboto.render(f"Unshown reports: {len(city.reports)-i}", True, (0,0,0))
            win.blit(text_extra, (width/2-85, 530))                                     # "x more tasks" text
            break

    # Draws a full report
def draw_full_report(win, mouse, report):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    lst = str(report).split(".")
    part1 = roboto.render(lst[0], True, (0,0,0))
    win.blit(part1, (width/2-130,height/2-258))
    for part, i in zip(lst[1:5],range(4)):
        for line, j in zip(part.split("\n"), range(len(part.split("\n")))):
            txt = roboto.render(line, True, (0,0,0))
            win.blit(txt, (width/2-320+160*i,height/2-210+j*50))
    luck = lst[5]
    if len(lst) > 6:
        luck += "." + lst[6]
    part2 = roboto.render(luck, True, (0,0,0))
    win.blit(part2, (width/2-200, height/2+170))

    # Draws map with cities 
def draw_map(win, mouse, world, topleft=None):
    if topleft==None:
        topleft=(-3,-2)
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    for i in range(7):
        for j in range(5):
            pygame.draw.rect(win,(0,0,0),[width/2-350+i*100,height/2-280+j*100,100,100], 1)
            if world.map[(topleft[0] + i, topleft[1]+j)] != "Empty":                                                            # Draws cities on map (just text for now)
                txt = roboto.render("City", True, (0,0,0))
                win.blit(txt, (width/2-340+i*100,height/2-230+j*100))
            if width/2-350+i*100 <= mouse[0] <= width/2-250+i*100 and height/2-280+j*100 <= mouse[1] <= height/2-180+j*100:
                pygame.draw.rect(win,(255,205,50),[width/2-350+i*100,height/2-280+j*100,100,100], 2)

    # Draws possible actions on main menu based on selected item (text)
def draw_actions(win, selected, view):
    if isinstance(selected, Report):
        if view == 1:
            view_text = pacifico.render("View", True, (0,0,0))
            win.blit(view_text, (width/2-255, height-105))
            delete_text = pacifico.render("Delete", True, (0,0,0))
            win.blit(delete_text, (width/2-115, height-105))
            mark_as_read_text = pacifico_small.render("Mark as Read", True, (0,0,0))
            win.blit(mark_as_read_text, (width/2+5, height-97))
        else:
            back_text = pacifico.render("Back", True, (0,0,0))
            win.blit(back_text, (width/2-255, height-105))
            delete_text = pacifico.render("Delete", True, (0,0,0))
            win.blit(delete_text, (width/2-115, height-105))
    elif isinstance(selected, City):                                                # Make attack text only visible only if city owner != player
        if view == 3:
            attack_text = pacifico.render("Attack", True, (0,0,0))
            win.blit(attack_text, (width/2-270, height-105))
            raid_text = pacifico.render("Raid", True, (0,0,0))
            win.blit(raid_text, (width/2-115, height-105))
            spy_text = pacifico.render("Spy", True, (0,0,0))
            win.blit(spy_text, (width/2+45, height-105))
            conq_text = pacifico.render("Conquer", True, (0,0,0))
            win.blit(conq_text, (width/2+175, height-105))
        elif view == 5:
            attack_text = pacifico.render("Send army", True, (0,0,0))
            win.blit(attack_text, (width/2-298, height-105))
    elif isinstance(selected, Building):
        if selected.type == "Empty":
            build_text = pacifico.render("Build", True, (0,0,0))
            win.blit(build_text, (width/2-260, height-105))
        elif selected.level < 5:
            upgrade_text = pacifico.render("Upgrade", True, (0,0,0))
            win.blit(upgrade_text, (width/2-280, height-105))
        if selected.type in ["Training Camp", "Factory", "Agency", "Military HQ", "Range"]:
            train_text = pacifico.render("Train", True, (0,0,0))
            win.blit(train_text, (width/2-115, height-105))

    # Draws menu where player chooses troops --- Make it display destination as well!!!!!
def draw_attack_menu(win, mouse, city, task):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)         # Border
    for key, i in zip(task.data[0].units, range(5)):
        # Unit names and counts
        txt = roboto.render(f"{key}:", True, (0,0,0))
        win.blit(txt, (width/2-300, height/2-240 + 95*i))
        val = roboto.render(f"{task.data[0].units[key]}", True, (0,0,0))
        win.blit(val, (width/2-150, height/2-240 + 95*i))
        txt_avail = roboto.render(f"Available: {city.army.units[key]}", True, (0,0,0))
        win.blit(txt_avail, (width/2-300, height/2-215 + 95*i))
        
        # Buttons
        for j in range(6):
            pygame.draw.rect(win,(0,0,0),[width/2-102+j*70,height/2-247+95*i,54,54], 2) 
            if width/2-102+j*70 <= mouse[0] <= width/2-48+j*70 and height/2-247+95*i <= mouse[1] <= height/2-193+95*i:
                pygame.draw.rect(win,(250,205,50),[width/2-102+j*70,height/2-247+95*i,54,54], 2)
        # Text
        txt_m1 = roboto.render("-1", True, (0,0,0))
        win.blit(txt_m1, (width/2-85, height/2-235 + 95*i))
        txt_0 = roboto.render("0", True, (0,0,0))
        win.blit(txt_0, (width/2-15, height/2-235 + 95*i))
        txt_p1 = roboto.render("+1", True, (0,0,0))
        win.blit(txt_p1, (width/2+50, height/2-235 + 95*i))
        txt_p10 = roboto.render("+10", True, (0,0,0))
        win.blit(txt_p10, (width/2+115, height/2-235 + 95*i))
        txt_p100 = roboto.render("+100", True, (0,0,0))
        win.blit(txt_p100, (width/2+180, height/2-235 + 95*i))
        txt_max = roboto.render("MAX", True, (0,0,0))
        win.blit(txt_max, (width/2+250, height/2-235 + 95*i))
        
    # Draws start menu for setting up and starting a game
def draw_start_menu(win, mouse):
    citywars_text = pacifico_huge.render("City Wars", True, (0,0,0))
    win.blit(citywars_text, (300, 25))
    # Borders
    pygame.draw.rect(win,(0,0,0),[width/2-172,height/2-152,344,104], 2)
    pygame.draw.rect(win,(0,0,0),[width/2-172,height/2-27,344,104], 2)
    pygame.draw.rect(win,(0,0,0),[width/2-172,height/2+98,344,104], 2)
    if width/2-172 <= mouse[0] <= width/2+172 and height/2-152 <= mouse[1] <= height/2-48:
        pygame.draw.rect(win,(255,250,205),[width/2-172,height/2-152,344,104], 2)
    elif width/2-172 <= mouse[0] <= width/2+172 and height/2-27 <= mouse[1] <= height/2+77:
        pygame.draw.rect(win,(255,250,205),[width/2-172,height/2-27,344,104], 2)
    elif width/2-172 <= mouse[0] <= width/2+172 and height/2+98 <= mouse[1] <= height/2 +202:
        pygame.draw.rect(win,(255,250,205),[width/2-172,height/2+98,344,104], 2)
    
    # Text
    new_sp_text = pacifico.render("New Game (Singleplayer)", True, (0,0,0))
    win.blit(new_sp_text, (width/2-165, height/2-130))
    new_mp_text = pacifico.render("New Game (Multiplayer)", True, (0,0,0))
    win.blit(new_mp_text, (width/2-160, height/2-3))
    new_sp_text = pacifico.render("Load Game", True, (0,0,0))
    win.blit(new_sp_text, (width/2-55, height/2+122))

    # Draws menu on the right in city view
def draw_training_menu(win, mouse, task, err):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Text
    train = roboto.render("Training", True, (0,0,0))
    win.blit(train, (width-180, 180))
    unit_txt = roboto.render(f"Unit: {task.data[0]}", True, (0,0,0))
    win.blit(unit_txt, (width-210, 205))
    amount = roboto.render(f"Amount: {task.data[1]}", True, (0,0,0))
    win.blit(amount, (width-210, 230))

    # Error
    e = roboto.render(err, True, (255, 0, 0))
    win.blit(e, (width-210, 570))

    # Buttons
    pygame.draw.rect(win,(255,255,255),[width-187,370,50,50], 2)          # B-1
    if width-187 <= mouse[0] <= width-137 and 370 <= mouse[1] <= 420:
        pygame.draw.rect(win,(250,205,50),[width-187,370,50,50], 2)        # B-1
    pygame.draw.rect(win,(255,255,255),[width-117,370,50,50], 2)          # B0
    if width-117 <= mouse[0] <= width-67 and 370 <= mouse[1] <= 420:
        pygame.draw.rect(win,(250,205,50),[width-117,370,50,50], 2)          # B0
    pygame.draw.rect(win,(255,255,255),[width-187,430,50,50], 2)          # B+1
    if width-187 <= mouse[0] <= width-137 and 430 <= mouse[1] <= 480:
        pygame.draw.rect(win,(250,205,50),[width-187,430,50,50], 2)          # B+1
    pygame.draw.rect(win,(255,255,255),[width-117,430,50,50], 2)          # B+10
    if width-117 <= mouse[0] <= width-67 and 430 <= mouse[1] <= 480:
        pygame.draw.rect(win,(250,205,50),[width-117,430,50,50], 2)          # B+10
    pygame.draw.rect(win,(255,255,255),[width-202,490,150,50], 2)          # B confirm
    if width-202 <= mouse[0] <= width-52 and 490 <= mouse[1] <= 540:
        pygame.draw.rect(win,(250,205,50),[width-202,490,150,50], 2)          # B confirm

    # Text in buttons
    m1 = roboto.render("-1", True, (0,0,0))
    win.blit(m1, (width-170, 385))
    unit_txt = roboto.render("+1", True, (0,0,0))
    win.blit(unit_txt, (width-100, 385))
    m10 = roboto.render("-10", True, (0,0,0))
    win.blit(m10, (width-180, 445))
    p10 = roboto.render("+10", True, (0,0,0))
    win.blit(p10, (width-110, 445))
    confirm = pacifico.render("Confirm", True, (0,0,0))
    win.blit(confirm, (width-178, 482))

    # Draws menu on the right in city view
def draw_building_menu(win, mouse, task, err, b_page):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Top text
    txt = task.data[0] if task.data[0] != "Empty" else ""
    b_text = roboto.render("Building "+txt, True, (0,0,0))
    win.blit(b_text, (width-210, 180))

    # Option buttons and text
    for b, i in zip(building_costs, range(len(building_costs))):
        if i in range(8*(b_page), 8*(b_page+1)):
            pygame.draw.rect(win,(255,255,255),[width-205,210+30*(i%8),160,28], 2)
            if width-205 <= mouse[0] <= width-45 and 210+30*(i%8) <= mouse[1] <= 238+30*(i%8):
                pygame.draw.rect(win,(250,205,50),[width-205,210+30*(i%8),160,28], 2)
            txt = b_text = roboto_small.render(b, True, (0,0,0))
            win.blit(txt, (width-160, 215+30*(i%8)))

    # Next and prev page buttons
    pygame.draw.rect(win,(255,255,255),[width-195,455,68,25], 2)          # B-1
    if width-195 <= mouse[0] <= width-137 and 455 <= mouse[1] <= 480:
        pygame.draw.rect(win,(250,205,50),[width-195,455,68,25], 2)        # B-1
    pygame.draw.rect(win,(255,255,255),[width-125,455,68,25], 2)          # B0
    if width-125 <= mouse[0] <= width-67 and 455 <= mouse[1] <= 480:
        pygame.draw.rect(win,(250,205,50),[width-125,455,68,25], 2)          # B0
    
    # Confirm button
    pygame.draw.rect(win,(255,255,255),[width-202,490,150,50], 2)          # B confirm
    if width-202 <= mouse[0] <= width-52 and 490 <= mouse[1] <= 540:
        pygame.draw.rect(win,(250,205,50),[width-202,490,150,50], 2)          # B confirm

    # Next, prev and confirm text
    prev = roboto_small.render("Prev", True, (0,0,0))
    win.blit(prev, (width-180, 460))
    next = roboto_small.render("Next", True, (0,0,0))
    win.blit(next, (width-110, 460))
    confirm = pacifico.render("Confirm", True, (0,0,0))
    win.blit(confirm, (width-178, 482))

    # Error
    e = roboto.render(err, True, (255, 0, 0))
    win.blit(e, (width-210, 570))






# Updates display (GUI)
def redraw_window(win, view, mouse, selected, city, topleft, task, err, b_page):
    if view == 0:
        win.fill((255, 255, 255))
        draw_start_menu(win, mouse)
    if view == 1: 
        win.fill((255,0,0))
        draw_reports(win, mouse, city)
        draw_bottom_menu(win, mouse, (255, 100, 100))
        draw_next_turn_button(win, mouse, (255, 100, 100))
    elif view == 2:
        win.fill((0,255,0))
        if task != None:
            if task.type == "Train":
                draw_training_menu(win, mouse, task, err)
            if task.type == "Build":
                draw_building_menu(win, mouse, task, err, b_page)
        draw_res(win, city)
        draw_city(win, mouse, city)
        draw_tasks(win, mouse, city)
        draw_bottom_menu(win, mouse, (100, 255, 100))
        draw_next_turn_button(win, mouse, (100, 255, 100))
    elif view == 3:
        win.fill((0,0,255))
        draw_map(win, mouse, world1, topleft)
        draw_map_move_buttons(win, mouse)
        draw_bottom_menu(win, mouse, (100, 100, 255))
        draw_next_turn_button(win, mouse, (100, 100, 255))
    elif view == 4:
        win.fill((255,0,0))
        draw_full_report(win, mouse, selected)
        draw_bottom_menu(win, mouse, (255, 100, 100))
    elif view == 5:
        win.fill((0,0,255))
        draw_attack_menu(win, mouse, city, task)
        draw_tasks(win, mouse, city)
        draw_bottom_menu(win, mouse, (100, 100, 255))
    draw_actions(win, selected, view)
    draw_top_menu(win, mouse)
    pygame.display.update()



# Main function
def main():
    run = True
    clock = pygame.time.Clock()
    view = 0
    selected = None
    city = world1.map[ca]
    topleft = (-3, -2)
    task = None
    err = ""
    b_page = 0

    while run:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        redraw_window(win, view, mouse, selected, city, topleft, task, err, b_page)
        
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Changing view / quitting
                if view != 0:               # Can't change views if no game is running!
                    if width-100 <= mouse[0] <= width and 0 <= mouse[1] <= 25:
                        run = False
                        pygame.quit()
                    elif width-200 <= mouse[0] <= width-100 and 0 <= mouse[1] <= 25:
                        view = 1
                        selected, task, err = None, None, ""
                    elif width-300 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 25:
                        view = 2
                        selected, task, err = None, None, ""
                    elif width-400 <= mouse[0] <= width-300 and 0 <= mouse[1] <= 25:
                        view = 3
                        selected, task, err = None, None, ""

                # Main menu actions
                if isinstance(selected, Report):
                    if view == 1:
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = 4
                            selected.read = True
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            city.reports.remove(selected)
                            selected = None
                        elif width/2 <= mouse[0] <= width/2+150 and height-100 <= mouse[1] <= height-50:            # Menu button 3
                            selected.read = True
                    elif view == 4:
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = 1
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            view = 1
                            city.reports.remove(selected)
                            selected = None
                elif isinstance(selected, City):
                    if view == 3:
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = 5
                            task = Task("Move Troops", [Army(), city, selected, "Attack"], 2)                                       # Change end turn calculation
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            view = 5
                            task = Task("Move Troops", [Army(), city, selected, "Raid"], 2)                                       # Change end turn calculation
                        elif width/2 <= mouse[0] <= width/2+150 and height-100 <= mouse[1] <= height-50:            # Menu button 3
                            view = 5
                            task = Task("Move Troops", [Army(), city, selected, "Espionage"], 2)                                       # Change end turn calculation
                        elif width/2+150 <= mouse[0] <= width/2+300 and height-100 <= mouse[1] <= height-50:        # Menu button 4
                            view = 5
                            task = Task("Move Troops", [Army(), city, selected, "Conquest"], 2)                                       # Change end turn calculation
                elif isinstance(selected, Building):
                    if selected.type == "Empty":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            task = Task("Build", ["Empty", selected.slot], 2)                                                     # Change end turn calculation
                            pass
                    elif selected.level < 5:
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            # Upgrade the building
                            pass
                    if selected.type in ["Training Camp", "Factory", "Range", "Military HQ", "Agency"]:
                        helper_dict = {"Training Camp": "Infantryman", "Range": "Sniper", "Factory": "Tank", "Agency": "Spy", "Military HQ": "General"}
                        if width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:              # Menu button 2
                            task = Task("Train", [helper_dict[selected.type], 0], 2)                                                    # Change end turn calculation
                            
            
                # View-specific actions
                if view == 0:
                    if width/2-172 <= mouse[0] <= width/2+172 and height/2-152 <= mouse[1] <= height/2-48:
                        view = 2
                        # Username prompt, start game
                    elif width/2-172 <= mouse[0] <= width/2+172 and height/2-27 <= mouse[1] <= height/2+77:
                        # Multiplayer settings page
                        pass
                    elif width/2-172 <= mouse[0] <= width/2+172 and height/2+98 <= mouse[1] <= height/2 +202:
                        # List saves and load game
                        pass
                if view == 1:
                    for i in range(min(8, len(city.reports))):
                        if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+i*50 <= mouse[1] <= height/2-227+i*50:
                            selected, task = city.reports[i], None
                elif view == 2:
                    if city.size == 6:
                        x, y = (3, 2)
                        for i in range(x):
                            for j in range(y):
                                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-180+j*150 <= mouse[1] <= height/2-30+j*150:
                                    selected, task = city.buildings[3*j + i + 1], None
                    elif city.size == 9:
                        x, y = (3, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task = city.buildings[3*j + i + 1], None
                    elif city.size == 12:
                        x, y = (4, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-300+i*150 <= mouse[0] <= width/2-150+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task = city.buildings[4*j + i + 1], None
                    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:
                        selected, task = city.buildings[0], None
                    if task != None:
                        if task.type == "Train":
                            #                                                                                        Make it check for resources and housing!
                            if width-187 <= mouse[0] <= width-137 and 370 <= mouse[1] <= 420:
                                if task.data[1] - 1 >= 0:
                                    task.data[1] -= 1
                                    err = ""
                            if width-117 <= mouse[0] <= width-67 and 370 <= mouse[1] <= 420:
                                task.data[1] += 1
                                res, err = city.required_res(task), ""
                                if task.data[1] + city.army.count() > 75 + values.housing_capacity[city.find_level("Housing")]:
                                    err = "Not enough space!" 
                                    task.data[1] -= 1
                                elif res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                    err = "Need more resources!"
                                    task.data[1] -= 1
                            if width-187 <= mouse[0] <= width-137 and 430 <= mouse[1] <= 480:
                                if task.data[1] - 10 >= 0:
                                    task.data[1] -= 10
                            if width-117 <= mouse[0] <= width-67 and 430 <= mouse[1] <= 480:
                                task.data[1] += 10
                                res, err = city.required_res(task), ""
                                if task.data[1] + city.army.count() > 75 + values.housing_capacity[city.find_level("Housing")]:
                                    err = "Not enough space!" 
                                    task.data[1] -= 10
                                elif res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                    err = "Need more resources!"
                                    task.data[1] -= 10
                            if width-202 <= mouse[0] <= width-52 and 490 <= mouse[1] <= 540:
                                err = ""
                                # Confirm task and add to current tasks
                                pass
                        
                        # Building
                        elif task.type == "Build":

                            # Building selection
                            for b, i in zip(building_costs, range(len(building_costs))):
                                if i in range(8*(b_page), 8*(b_page+1)):
                                    if width-205 <= mouse[0] <= width-45 and 210+30*(i%8) <= mouse[1] <= 238+30*(i%8):
                                        task.data[0], err = b, ""
                            
                            # Prev/Next button
                            if width-195 <= mouse[0] <= width-137 and 455 <= mouse[1] <= 480:
                                b_page, err = 0, ""
                            if width-125 <= mouse[0] <= width-67 and 455 <= mouse[1] <= 480:
                                b_page, err = 1, ""

                            # Confirmation
                            if width-202 <= mouse[0] <= width-52 and 490 <= mouse[1] <= 540:
                                if task.data[0] == "Empty":
                                    err = "Select building!"
                                elif task.data[0] in [b.type for b in list(city.buildings.values())]:
                                    err = "Already built!"
                                else:
                                    res, err = city.required_res(task), ""
                                    if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                        err = "Need more resources!"
                                    else:
                                        err = ""
                                        # Confirm task and add to current tasks

                elif view == 3:
                    # Selecting a city:
                    x, y = (7, 5)
                    for i in range(x):
                        for j in range(y):
                            if width/2-350+i*100 <= mouse[0] <= width/2-250+i*100 and height/2-280+j*100 <= mouse[1] <= height/2-180+j*100:
                                if world1.map[(topleft[0]+i,topleft[1]+j)] != "Empty":
                                    selected = world1.map[(topleft[0]+i,topleft[1]+j)]                                   # Figure out where to show map first (coords)
                    # Map movement
                    if width-150 <= mouse[0] <= width-100 and height-202 <= mouse[1] <= height-152:
                        if topleft[1] > -world1.size:
                            topleft = (topleft[0], topleft[1] - 1)
                    elif width-150 <= mouse[0] <= width-100 and height-98 <= mouse[1] <= height-48:    
                        if topleft[1] < world1.size-4:
                            topleft = (topleft[0], topleft[1] + 1)
                    elif width-202 <= mouse[0] <= width-152 and height-150 <= mouse[1] <= height-100:
                        if topleft[0] > -world1.size:
                            topleft = (topleft[0]-1, topleft[1])
                    elif width-98 <= mouse[0] <= width-48 and height-150 <= mouse[1] <= height-100:
                        if topleft[0] < world1.size - 6:
                            topleft = (topleft[0]+1, topleft[1])

                elif view == 5:
                    # Unit selection
                    for unit, i in zip(Army().units, range(5)): # For each line
                        for change, j in zip([-1, -task.data[0].units[unit], 1, 10, 100, city.army.units[unit]], range(6)): # for each column
                            if width/2-102+j*70 <= mouse[0] <= width/2-48+j*70 and height/2-247+95*i <= mouse[1] <= height/2-193+95*i: # If clicked
                                if 0 <= task.data[0].units[unit] + change <= city.army.units[unit]:    # If enough troops and not going below 0
                                    task.data[0].units[unit] += change         # Add troops 
                    






                    



'''
tasks = [Task(type="Build", data=["Iron Mine", 2], end_turn=3), Task(type="Upgrade",data=["Iron Mine"], end_turn=2), Task(type="Train", data=["Spy", 5], end_turn=7)]
tasks2 = [Task(type="Build", data=["Iron Mine", 2], end_turn=3),Task(type="Upgrade",data=["Iron Mine"], end_turn=2), Task(type="Train",data=["Spy", 5], end_turn=7), Task(type="Move Troops", data=[Army([10, 10, 0, 0, 0]), world1.map[ca], world1.map[cd], "Attack"], end_turn=9)]
'''


main()
