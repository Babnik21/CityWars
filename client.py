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

    # Draws text on screen
def draw_text(strings, poss, font, c):
    for string, pos in zip(strings, poss):
        txt = font.render(string, True, c)
        win.blit(txt, pos)

def draw_h_rect(win, mouse, pos, c1, c2, border = 0):
    pygame.draw.rect(win,c1,pos, border)
    if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1]+pos[3]:
        pygame.draw.rect(win,c2,pos, border)

    # Draws next turn button in bottom left of the screen
def draw_next_turn_button(win, mouse, c):
    c2 = tuple([color + 50 if color < 205 else 255 for color in c])         # Color
    draw_h_rect(win, mouse, [23,580,204,50], c, c2)                         # Highlightable rect
    pygame.draw.rect(win,(255,255,255),[23,580,204,50], 2)                  # Border
    draw_text(["Next Turn"], [(55, 575)], pacifico, (0,0,0))                # Text

# Funciton that draws the menu at top right of the screen (rectangles + text)
def draw_top_menu(win, mouse):
    # Rectangles
    for i in range(4):
        draw_h_rect(win, mouse, [width-100*(i+1),0,100,25], (20, 20, 20), (50, 50, 50))

    # Text
    strs = "Exit", "Reports", "City", "Map"
    poss = (width-65,0), (width-185,0), (width-270,0), (width-370,0)
    draw_text(strs, poss, roboto, (255, 255, 255))
    
# Draws bottom menu in city view
def draw_bottom_menu(win, mouse, c):
    pygame.draw.rect(win, (0,0,0), [width/2-300-2,height-100-2,604,54], 2)      # Border
    c2 = tuple([color + 50 if color < 205 else 255 for color in c])       # Change color for highlighted option
    for i in range(4):
        draw_h_rect(win, mouse, [width/2-300+(150*i),height-100,150,50], c, c2)

# Draws map movement buttons ------                 (text needs to be added)
def draw_map_move_buttons(win, mouse):
    # Rectangles
    for i, j in zip([-1, 0, 0, 1], [0, -1, 1, 0]):
        draw_h_rect(win, mouse, [width-150+52*i,height-150+52*j,50,50], (100, 100, 255), (150, 150, 255))

    # Borders 
    pygame.draw.rect(win,(0,0,0),[width-152,height-204,54,54],2)     # Up arrow rect
    pygame.draw.rect(win,(0,0,0),[width-152,height-100,54,54],2)     # Down arrow rect
    pygame.draw.rect(win,(0,0,0),[width-204,height-152,54,54],2)     # Left arrow tect
    pygame.draw.rect(win,(0,0,0),[width-100,height-152,54,54],2)     # Right arrow rect

    # Draws resource display
def draw_res(win, city):
    pygame.draw.rect(win,(255,255,255),[width-227,55,204,110], 2)          # Border
    food = f"Food: {city.resources[0]}/{200+values.warehouse_capacity[city.find_level('Warehouse')]}"
    iron = f"Iron: {city.resources[1]}/{200+values.warehouse_capacity[city.find_level('Warehouse')]}"
    gold = f"Gold: {city.resources[2]}/{10+values.bank_capacity[city.find_level('Bank')]}"
    hous = f"Housing: {city.army.count()}/{75+values.housing_capacity[city.find_level('Housing')]}"
    poss = (width-210, 60), (width-210, 85), (width-210, 110), (width-210, 135)
    draw_text([food, iron, gold, hous], poss, roboto, (0,0,0))

    # Draws city (just building outlines for now)
def draw_city(win, mouse, city):
    pygame.draw.rect(win,(255,255,255),[width/2-352,height/2-282,704,504], 2)       # Border
    # Wall
    string = f"Wall level {city.find_level('Wall')}"
    draw_text([string], [(width/2-70, 520)], pacifico_small, (0,0,0))

    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:     # Wall
        pygame.draw.rect(win, (255, 250, 205), [width/2-300, height/2+195, 600, 25], 2)
    if city.size == 6:
        x, y = (3, 2)
        for i in range(x):
            for j in range(y):
                draw_h_rect(win, mouse, [width/2-225+i*150,height/2-180+j*150,150,150], (50,200,50), (255,250,205), border=2)
                string = city.buildings[3*j + i + 1].type
                draw_text([string], [(width/2-225+i*150, height/2-145+j*150)], pacifico, (0,0,0))
    elif city.size == 9:
        x, y = (3, 3)
        for i in range(x):
            for j in range(y):
                draw_h_rect(win, mouse, [width/2-225+i*150,height/2-255+j*150,150,150], (50,200,50), (255,250,205), border=2)
                string = city.buildings[3*j + i + 1].type
                draw_text([string], [(width/2-225+i*150, height/2-220+j*150)], pacifico, (0,0,0))
    elif city.size == 12:
        x, y = (4, 3)
        for i in range(x):
            for j in range(y):
                draw_h_rect(win, mouse, [width/2-300+i*150,height/2-255+j*150,150,150], (50,200,50), (255,250,205), border=2)
                string = city.buildings[4*j + i + 1].type
                draw_text([string], [(width/2-300+i*150, height/2-220+j*150)], pacifico, (0,0,0))

    # Draws tasks
def draw_tasks(win, mouse, city):
    c_tasks, o_tasks = city.current_tasks, city.ongoing_tasks
    pygame.draw.rect(win,(255,255,255),[23,55,204,504], 2)          # Border
    strings, poss = ["Current"], [(28, 58)]
    offset = 25
    #Current tasks
    for task in c_tasks:
        h=offset
        string = str(task)
        for line in string.split("\n"):
            strings.append(line)
            poss.append((30, 60 + offset))
            offset += 20
        offset += 10
        pygame.draw.rect(win, (20, 20, 20), [28,55+h, 194, offset-h-2], 2)      # Task border
    strings.append("Ongoing")
    poss.append((28, 58 + offset))
    offset += 25
    #Ongoing tasks
    for i in range(len(o_tasks)):
        h=offset
        string = str(o_tasks[i])
        if offset + 10 + 20 * len(string.split("\n")) > 500:
            # Draw "x more tasks"
            strings.append(f"Unshown tasks: {len(o_tasks)-i}")
            poss.append((30, 535))
            break 
        for line in string.split("\n"):
            # task text
            strings.append(line)
            poss.append((30, 60 + offset))
            offset += 20
        offset += 10
        pygame.draw.rect(win, (20, 20, 20), [28,55+h, 194, offset-h-2], 2)      # Task border
    draw_text(strings, poss, roboto, (0,0,0))

    # Draws reports
def draw_reports(win, mouse, city):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    offset = 0
    strings, poss = [], []
    for i in range(len(city.reports)):
        temp = str(city.reports[i]).split(".")
        draw_h_rect(win, mouse, [width/2-347,height/2-277+offset,694,50], (0,0,0), (212,175,55), border=2)
        strings.append(temp[0])
        poss.append((width/2-340,height/2-265+offset))
        offset += 52
        if offset >= 460:
            strings.append(f"Unshown reports: {len(city.reports)-i}")
            poss.append((width/2-85, 530))
            break
    draw_text(strings, poss, roboto, (0,0,0))

    # Draws a full report
def draw_full_report(win, mouse, report):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    lst = str(report).split(".")
    strings, poss = [lst[0]], [(width/2-130,height/2-258)]
    for part, i in zip(lst[1:5],range(4)):
        for line, j in zip(part.split("\n"), range(len(part.split("\n")))):
            strings.append(line)
            poss.append((width/2-320+160*i,height/2-210+j*50))
    luck = lst[5] if len(lst) <= 5 else lst[5] + "." + lst[6]
    strings.append(luck)
    poss.append((width/2-200, height/2+170))
    draw_text(strings, poss, roboto, (0,0,0))

    # Draws map with cities 
def draw_map(win, mouse, world, topleft=None):
    if topleft==None:
        topleft=(-3,-2)
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    for i in range(7):
        for j in range(5):
            draw_h_rect(win, mouse, [width/2-350+i*100,height/2-280+j*100,100,100], (0,0,0), (255,250,205), border=1)
            if world.map[(topleft[0] + i, topleft[1]+j)] != "Empty":                                                            # Make it print something other than "City"
                draw_text(["City"], [(width/2-340+i*100,height/2-230+j*100)], roboto, (0,0,0))

    # Draws possible actions on main menu based on selected item (text)
def draw_actions(win, selected, view):
    strings = []
    poss = []
    if isinstance(selected, Report):
        if view == 1:
            strings = ["View", "Delete", "Mark as Read"]
            poss = [(width/2-255, height-105), (width/2-115, height-105), (width/2+5, height-97)]
        else:
            strings = ["Back", "Delete"]
            poss = [(width/2-255, height-105), (width/2-115, height-105)]
    elif isinstance(selected, City):                                                # Make attack text only visible only if city owner != player
        if view == 3:
            strings = ["Attack", "Raid", "Spy", "Conquer"]
            poss = [(width/2-270, height-105), (width/2-115, height-105), (width/2+45, height-105), (width/2+175, height-105)]
        elif view == 5:
            strings = ["Send Army"]
            poss = [(width/2-298, height-105)]
    elif isinstance(selected, Building):
        if selected.type == "Empty":
            strings = ["Build"]
            poss = [(width/2-260, height-105)]
        elif selected.level < 5:
            strings = ["Upgrade"]
            poss = [(width/2-280, height-105)]
        if selected.type in ["Training Camp", "Factory", "Agency", "Military HQ", "Range"]:
            strings.append("Train")
            poss.append((width/2-115, height-105))
    draw_text(strings, poss, pacifico, (0,0,0))

    # Draws menu where player chooses troops --- Make it display destination as well!!!!!
def draw_attack_menu(win, mouse, city, task):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)         # Border
    for key, i in zip(task.data[0].units, range(5)):
        # Unit names and counts
        strings = [f"{key}:", f"{task.data[0].units[key]}", f"Available: {city.army.units[key]}"]
        poss = [(width/2-300, height/2-240 + 95*i), (width/2-150, height/2-240 + 95*i), (width/2-300, height/2-215 + 95*i)]
        
        
        # Buttons
        for j in range(6):
            draw_h_rect(win, mouse, [width/2-102+j*70,height/2-247+95*i,54,54], (0,0,0), (250, 205, 50), border=2)

        # Text
        strings += ["-1", "0", "+1", "+10", "+100", "MAX"]
        poss += [(width/2-85, height/2-235 + 95*i), (width/2-15, height/2-235 + 95*i), (width/2+50, height/2-235 + 95*i),(width/2+115, height/2-235 + 95*i),(width/2+180, height/2-235 + 95*i),(width/2+250, height/2-235 + 95*i)]
        draw_text(strings, poss, roboto, (0,0,0))
        
    # Draws start menu for setting up and starting a game
def draw_start_menu(win, mouse):
    # Borders
    for i in range(3):
        draw_h_rect(win, mouse, [width/2-172,height/2-152+125*i,344,104], (0,0,0), (255, 250, 205), border=2)
    
    # Text
    strings = ["New Game (Singleplayer)","New Game (Multiplayer)","Load Game"]
    poss = [(width/2-165, height/2-130),(width/2-160, height/2-3),(width/2-65, height/2+122)]
    draw_text(strings, poss, pacifico, (0,0,0))
    draw_text(["City Wars"], [(300, 25)], pacifico_huge, (0,0,0))

    # Draws menu on the right in city view
def draw_training_menu(win, mouse, task, err):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Top text
    strings = ["Training", f"Unit: {task.data[0]}", f"Amount: {task.data[1]}"]
    poss = [(width-180, 180), (width-210, 205), (width-210, 230)]
    
    draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))       # Error text in red

    # Buttons
    for i in range(4):
        draw_h_rect(win, mouse, [width-187+70*(i%2),370+60*(i//2),50,50], (255, 255, 255), (250, 202, 50), border=2)           # Delete commented stuff
    '''pygame.draw.rect(win,(255,255,255),[width-187,370,50,50], 2)          # B-1
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
        pygame.draw.rect(win,(250,205,50),[width-202,490,150,50], 2)          # B confirm'''

    # Text in buttons
    strings += ["-1", "+1", "-10", "+10"]
    poss += [(width-170, 385), (width-100, 385), (width-180, 445), (width-110, 445)]
    
    # Drawing text
    draw_text(strings, poss, roboto, (0,0,0))       # top + button text
    draw_text(["Confirm"], [(width-178, 482)], pacifico, (0,0,0))   # Confirm text

    # Draws menu on the right in city view
def draw_building_menu(win, mouse, task, err, b_page):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Top text
    string = "Building " + task.data[0] if task.data[0] != "Empty" else "Building"
    draw_text([string], [(width-210, 180)], roboto, (0,0,0))                            # Top text in roboto regular

    # Button text and positions
    strings_s, poss_s = [], []

    # Option buttons and text
    for b, i in zip(building_costs, range(len(building_costs))):
        if i in range(8*(b_page), 8*(b_page+1)):
            draw_h_rect(win, mouse, [width-205,210+30*(i%8),160,28], (255, 255, 255), (250, 205, 50), border=2)
            strings_s.append(b)
            poss_s.append((width-160, 215+30*(i%8)))

    # Next and prev page buttons
    for i in range(2):
        draw_h_rect(win, mouse, [width-195+70*i,455,68,25], (255, 255, 255), (250, 205, 50), border=2)
    
    # Confirm button
    draw_h_rect(win, mouse, [width-202,490,150,50], (255,255,255), (250,205,50), border=2)

    # Next, prev and confirm text
    strings_s += ["Prev", "Next"]
    poss_s += [(width-180, 460), (width-110, 460)]
    draw_text(strings_s, poss_s, roboto_small, (0,0,0))             # Small text (roboto): all buttons except confirm
    draw_text(["Confirm"], [(width-178, 482)], pacifico, (0,0,0))   # Confirm pacifico
    draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))       # Error




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
            if task.type == "Upgrade":
                draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))
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
    topleft = city.topleft_coords(world1)
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
                            task = Task("Upgrade", [selected.type], 2)
                            res, err = city.required_res(task), ""
                            if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                err = "Need more resources!"
                            else:                                                                                                       # Start task and deduct res
                                city.current_tasks.append(task)
                                city.spend_res(res)
                                selected, task = None, None
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
                                    selected, task, err = city.buildings[3*j + i + 1], None, ""
                    elif city.size == 9:
                        x, y = (3, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task, err = city.buildings[3*j + i + 1], None, ""
                    elif city.size == 12:
                        x, y = (4, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-300+i*150 <= mouse[0] <= width/2-150+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task, err = city.buildings[4*j + i + 1], None, ""
                    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:
                        selected, task, err = city.buildings[0], None, ""
                    if task != None:
                        if task.type == "Train":
                            err = ""
                            #                                                                                        Make it check for resources and housing!
                            if width-187 <= mouse[0] <= width-137 and 370 <= mouse[1] <= 420:
                                if task.data[1] - 1 >= 0:
                                    task.data[1] -= 1
                                    err = ""
                            if width-117 <= mouse[0] <= width-67 and 370 <= mouse[1] <= 420:
                                task.data[1] += 1
                                res, err = city.required_res(task), ""
                                if task.data[1] > city.calc_housing():
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
                                if task.data[1] > city.calc_housing():
                                    err = "Not enough space!" 
                                    task.data[1] -= 10
                                elif res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                    err = "Need more resources!"
                                    task.data[1] -= 10
                            if width-202 <= mouse[0] <= width-52 and 490 <= mouse[1] <= 540:
                                err = ""
                                if task in city.current_tasks:
                                    err = "Already training!"
                                else:
                                    city.current_tasks.append(task)
                                    city.spend_res(res)
                                    selected, task, err = None, None, ""
                        
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
                                elif task in city.current_tasks:
                                    err = "Already started!"
                                elif task.data[0] in [b.type for b in list(city.buildings.values())]:
                                    err = "Already built!"
                                else:
                                    res, err = city.required_res(task), ""
                                    if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                        err = "Need more resources!"
                                    else:
                                        city.current_tasks.append(task)
                                        city.spend_res(res)
                                        selected, task, err = None, None, ""

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
                    


main()
