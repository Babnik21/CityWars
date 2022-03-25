import pickle
import pygame
import sys
from module import *
from values import *
from os import listdir, remove
from os.path import isfile, join

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

def saves_list():
    files = [f for f in listdir("saves/.") if isfile(join("saves/.", f))]
    return files

    # Takes user input and returns it as string
def text_prompt(text, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:     # Check for backspace
            text = text[:-1]
        else:
            text += event.unicode
    return text

    # Draws text on screen
def draw_text(strings, poss, font, c):
    for string, pos in zip(strings, poss):
        txt = font.render(string, True, c)
        win.blit(txt, pos)

def draw_h_rect(win, mouse, pos, c1, c2, border = 0):
    pygame.draw.rect(win,c1,pos, border)
    if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1]+pos[3]:
        pygame.draw.rect(win,c2,pos, border)

def draw_current_turn(win, turn):
    draw_text([f"Current turn: {turn}"], [(25, 25)], roboto, (0,0,0))

def draw_image(win, path, pos, size):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
    win.blit(image, pos)

    # Draws next turn button in bottom left of the screen
def draw_next_turn_button(win, mouse, c):
    c2 = tuple([color + 50 if color < 205 else 255 for color in c])         # Color
    draw_h_rect(win, mouse, [23,580,204,50], c, c2)                         # Highlightable rect
    pygame.draw.rect(win,(255,255,255),[23,580,204,50], 2)                  # Border
    draw_text(["Next Turn"], [(55, 575)], pacifico, (0,0,0))                # Text

    # Funciton that draws the menu at top right of the screen (rectangles + text)
def draw_top_menu(win, mouse):
    # Rectangles
    for i in range(5):
        draw_h_rect(win, mouse, [width-100*(i+1),0,100,25], (20, 20, 20), (50, 50, 50))

    # Text
    strs = "Exit", "Reports", "City", "Map", "Overview"
    poss = (width-65,0), (width-185,0), (width-270,0), (width-370,0), (width-492, 0)
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
    for i, j, img in zip([-1, 0, 0, 1], [0, -1, 1, 0], ["arrow_left", "arrow_up", "arrow_down", "arrow_right"]):
        draw_h_rect(win, mouse, [width-150+52*i,height-150+52*j,50,50], (100, 100, 255), (150, 150, 255))
        draw_image(win, f"images/{img}.png", (width-145+52*i,height-145+52*j), (40,40))
        pygame.draw.rect(win,(0,0,0),[width-152+52*i,height-152+52*j,54,54],2)     # Right arrow rect

    # Draws resource display
def draw_res(win, city):
    pygame.draw.rect(win,(255,255,255),[width-227,55,204,110], 2)          # Border
    food = f"Food: {city.resources[0]}/{values.warehouse_capacity[city.find_level('Warehouse')]}"
    iron = f"Iron: {city.resources[1]}/{values.warehouse_capacity[city.find_level('Warehouse')]}"
    gold = f"Gold: {city.resources[2]}/{values.bank_capacity[city.find_level('Bank')]}"
    hous = f"Housing: {city.army.count()}/{values.housing_capacity[city.find_level('Housing')]}"
    poss = (width-210, 60), (width-210, 85), (width-210, 110), (width-210, 135)
    draw_text([food, iron, gold, hous], poss, roboto, (0,0,0))

    #Draws a building (displays image)
def draw_building(win, mouse, building, pos):
    # Ground (grey or green depending on building type)
    color = (50,204,73)
    pygame.draw.rect(win, color, [pos[0], pos[1], 150, 150])

    # Image
    draw_image(win, building.img, pos, (150, 150))

    # Level
    if building.type != "Empty":
        pygame.draw.circle(win, (255, 255, 255), (pos[0]+30, pos[1] + 30), 15)
        draw_text([str(building.level)], [(pos[0]+24, pos[1] + 18)], roboto, (0,0,0))

    # Highlighting border
    draw_h_rect(win, mouse, [pos[0],pos[1],150,150], color, (255,250,205), border=2)

    # Draws city 
def draw_city(win, mouse, city):
    pygame.draw.rect(win,(255,255,255),[width/2-352,height/2-282,704,504], 2)       # Border
    
    # Wall
    if city.find_level("Wall") > 0:
        image = pygame.image.load("images/wall.png")
        image = pygame.transform.scale(image, (700, 530))
        win.blit(image, (width/2-360, height/2-295))
        pygame.draw.circle(win, (255, 255, 255), (width/2, height/2+210), 15)
        #draw_text([str(city.find_level("Wall"))], [(width/2-6, height/2+198)], roboto, (0,0,0))

    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:     # Wall
        pygame.draw.rect(win, (255, 250, 205), [width/2-300, height/2+195, 600, 25], 2)

    strings, poss = [], []
    if city.size == 6:
        x, y = (3, 2)
        for i in range(x):
            for j in range(y):
                draw_building(win, mouse, city.buildings[3*j + i + 1], (width/2-225+i*150, height/2-180+j*150))
    elif city.size == 9:
        x, y = (3, 3)
        for i in range(x):
            for j in range(y):
                draw_building(win, mouse, city.buildings[3*j + i + 1], (width/2-225+i*150, height/2-255+j*150))
    elif city.size == 12:
        x, y = (4, 3)
        for i in range(x):
            for j in range(y):
                draw_building(win, mouse, city.buildings[4*j + i + 1], (width/2-300+i*150, height/2-255+j*150))

    # Text            
    draw_text(strings, poss, pacifico, (0,0,0))

    # Draws city points
def draw_points(city):
    draw_text([f"Points: {city.points}"], [(250, 25)], roboto, (0,0,0))

    # Draws tasks
def draw_tasks(win, mouse, city):
    c_tasks, o_tasks = city.current_tasks, city.ongoing_tasks
    pygame.draw.rect(win,(255,255,255),[23,55,204,504], 2)          # Border

    # Current tasks
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
        draw_h_rect(win, mouse, [199,58+h, 20, 20], (255,255,255), (250,205,50))
        draw_text(["x"], [(204,55+h)], roboto, (255, 0, 0))

    # Ongoing tasks
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

    # Text
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

    # Draws city details on the side menu (for map view)
def draw_city_info(win, selected):
    pygame.draw.rect(win,(255,255,255),[23,55,204,504], 2)          # Border
    if isinstance(selected, City):
        strings = [f"City: City Name", f"Points: {selected.points}", f"Owner: {selected.owner.username}", f"Coords: {selected.coords}"]
        poss = [(28, 58), (28, 88), (28, 118), (28, 148)]
        draw_text(strings, poss, roboto, (0,0,0))

    # Draws map with cities 
def draw_map(win, mouse, world, player, topleft=None):
    if topleft==None:
        topleft=(-3,-2)
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    pygame.draw.rect(win,(50,204,73),[width/2-350,height/2-280,700,500])       # Background
    for i in range(7):
        for j in range(5):
            draw_h_rect(win, mouse, [width/2-350+i*100,height/2-280+j*100,100,100], (0,0,0), (255,250,205), border=1)
            if isinstance(world.map[(topleft[0] + i, topleft[1]+j)], City):
                draw_image(win, "images/city.png", (width/2-350+i*100,height/2-280+j*100), (100, 100))
                pygame.draw.rect(win, (255,255,255),[width/2-345+i*100,height/2-278+j*100,90,18])
                draw_text(["CityName"], [(width/2-340+i*100,height/2-280+j*100)], roboto, (250,50,50))
                pygame.draw.ellipse(win, (255, 255, 255), (width/2-330+i*100,height/2-260+j*100, 40, 25))
                draw_text([str(world.map[(topleft[0] + i, topleft[1]+j)].points)], [(width/2-325+i*100,height/2-255+j*100)], roboto_small, (0,0,0))
            else:
                draw_image(win, f"images/{world.map[(topleft[0] + i, topleft[1]+j)]}.png", (width/2-350+i*100,height/2-280+j*100), (100, 100))

    # Draws possible actions on main menu based on selected item (text)
def draw_actions(win, selected, view):
    strings = []
    poss = []
    if isinstance(selected, Report):
        if view == "Reports main":
            strings = ["View", "Delete"]
            poss = [(width/2-255, height-105), (width/2-115, height-105)]
            draw_text(["Mark as read"], [(width/2+5, height-97)], pacifico_small, (0,0,0))
        else:
            strings = ["Back", "Delete"]
            poss = [(width/2-255, height-105), (width/2-115, height-105)]
    elif isinstance(selected, City):                                                # Make attack text only visible only if city owner != player
        if view == "Map":
            strings = ["Attack", "Raid", "Spy", "Conquer"]
            poss = [(width/2-270, height-105), (width/2-115, height-105), (width/2+45, height-105), (width/2+175, height-105)]
        elif view == "Troop select":
            strings = ["Send Army"]
            poss = [(width/2-298, height-105)]
        elif view == "Overview":
            strings = ["Go to", "Rename"]
            poss = [(width/2 - 280, height-105), (width/2 - 120, height-105)]
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
    for i in range(4):
        draw_h_rect(win, mouse, [width/2-172,height/2-152+110*i,344,104], (0,0,0), (255, 250, 205), border=2)
    
    # Text
    strings = ["New Game (Singleplayer)","New Game (Multiplayer)","Load Game", "Exit Game"]
    poss = [(width/2-165, height/2-130),(width/2-160, height/2-20),(width/2-65, height/2+90), (width/2-65, height/2+200)]
    draw_text(strings, poss, pacifico, (0,0,0))
    draw_text(["City Wars"], [(300, 25)], pacifico_huge, (0,0,0))

    # Draws overview page (cities list)
def draw_overview(win, mouse, player, page):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    strings, poss = [], []
    for i, city in enumerate(player.cities):
        if i in range(8*(page), 8*(page+1)):
            draw_h_rect(win, mouse, [width/2-347,height/2-277+52*(i%8),694,50], (0,0,0), (212,175,55), border=2)
            strings.append(str(city))
            poss.append((width/2-340,height/2-265+52*(i%8)))
    if len(player.cities) > 8:
        draw_h_rect(win, mouse, [width/2-100, 500, 80, 40], (0,0,0), (250, 205, 50), border=2)
        draw_h_rect(win, mouse, [width/2+20, 500, 80, 40], (0,0,0), (250, 205, 50), border=2)
        strings += ["Prev", "Next"]
        poss += [(width/2-80, 505), (width/2 + 40, 505)]
    draw_text(strings, poss, roboto, (0,0,0))

    # Draws menu on the right in city view
def draw_training_menu(win, mouse, task, err):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Top text
    strings = ["Training", f"Unit: {task.data[0]}", f"Amount: {task.data[1]}"]
    poss = [(width-180, 180), (width-210, 205), (width-210, 230)]
    
    draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))       # Error text in red

    # Buttons
    for i in range(4):
        draw_h_rect(win, mouse, [width-187+70*(i%2),270+60*(i//2),50,50], (255, 255, 255), (250, 205, 50), border=2)
    draw_h_rect(win, mouse, [width-202,490,150,50], (255, 255, 255), (250, 205, 50), border=2)

    # Text in buttons
    strings += ["-1", "+1", "-10", "+10"]
    poss += [(width-170, 285), (width-100, 285), (width-180, 345), (width-110, 345)]
    
    # Drawing text
    draw_text(strings, poss, roboto, (0,0,0))       # top + button text
    draw_text(["Confirm"], [(width-178, 482)], pacifico, (0,0,0))   # Confirm text

    # Draws menu on the right in city view
def draw_building_menu(win, mouse, task, err, page, city):
    pygame.draw.rect(win,(255,255,255),[width-227,175,204,384], 2)          # Border

    # Top text
    string = "Building " + task.data[0] if task.data[0] != "Empty" else "Building"
    draw_text([string], [(width-210, 180)], roboto, (0,0,0))                            # Top text in roboto regular

    # Button text and positions
    strings_s, poss_s = [], []

    # Option buttons and text
    for i, b in enumerate(building_costs):
        if i in range(8*(page), 8*(page+1)):
            draw_h_rect(win, mouse, [width-205,205+27*(i%8),160,25], (255, 255, 255), (250, 205, 50), border=2)
            strings_s.append(b)
            poss_s.append((width-160, 210+27*(i%8)))

    # Next and prev page buttons
    for i in range(2):
        draw_h_rect(win, mouse, [width-195+70*i,470,68,25], (255, 255, 255), (250, 205, 50), border=2)
    
    # Confirm button
    draw_h_rect(win, mouse, [width-202,500,150,50], (255,255,255), (250,205,50), border=2)

    # Next, prev and confirm text
    strings_s += ["Prev", "Next"]
    poss_s += [(width-180, 475), (width-110, 475)]
    draw_text(strings_s, poss_s, roboto_small, (0,0,0))             # Small text (roboto): all buttons except confirm
    draw_text(["Confirm"], [(width-178, 492)], pacifico, (0,0,0))   # Confirm pacifico
    draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))       # Error

    # Draws singleplayer game setup menu
def draw_sp_settings(win, mouse, err, username, num, selected):

    # Text input bar
    c = (255, 255, 255) if selected == "Text prompt" else (200, 200, 200)
    pygame.draw.rect(win,c,[0, 150, width, 25])                 # text prompt rect

    # Text data
    strings = ["Username: ", username, "Number of opponents: ", str(num), "Difficulty: (not yet)"]
    poss = [(150, 125), (150, 150), (150, 225), (150, 250), (150, 325)]

    # More/less players buttons
    strings += ["-", "+"]
    poss += [(215, 257), (265, 257)]
    draw_h_rect(win, mouse, (200, 250, 40, 40), (0,0,0), (250, 205, 50), 2)
    draw_h_rect(win, mouse, (250, 250, 40, 40), (0,0,0), (250, 205, 50), 2)

    #Printing text
    draw_text(strings, poss, roboto, (0,0,0))

    # Confirm button
    draw_h_rect(win, mouse, [width/2 - 100, 450, 200, 100], (0,0,0), (250, 205, 50), border = 2)
    draw_text(["Start game!"], [(width/2-80, 470)], pacifico, (0,0,0))
    
    # Error text
    draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))       

    # Draws task costs
def draw_costs(task, city):
    if task.data[0] != "Empty":
        res = city.required_res(task)
        c_res = (255, 0, 0) if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2] else (255, 255, 50)
        strings_s_res = ["Cost:", f"Food: {res[0]}", f"Iron: {res[1]}", f"Gold: {res[2]}"]
        poss_s_res = [(width-205, 420), (width - 160, 420), (width-160, 436), (width-160, 452)]
        draw_text(strings_s_res, poss_s_res, roboto_small, c_res)

    # Draws load menu
def draw_load_menu(win, mouse, page):
    pygame.draw.rect(win,(0,0,0),[width/2-352,height/2-282,704,504], 2)       # Border
    strings, poss = [], []
    saves = saves_list()
    for i, save in enumerate(saves):
        if i in range(8*(page), 8*(page+1)):
            draw_h_rect(win, mouse, [width/2-347,height/2-277+52*(i%8),694,50], (0,0,0), (212,175,55), border=2)
            strings.append(save)
            poss.append((width/2-340,height/2-265+52*(i%8)))
    if len(saves) > 8:
        draw_h_rect(win, mouse, [width/2-100, 500, 80, 40], (0,0,0), (250, 205, 50), border=2)
        draw_h_rect(win, mouse, [width/2+20, 500, 80, 40], (0,0,0), (250, 205, 50), border=2)
        strings += ["Prev", "Next"]
        poss += [(width/2-80, 505), (width/2 + 40, 505)]
    strings_p = ["Back", "Load", "Delete"]
    poss_p = [(width/2-210, height-105), (width/2-35, height-105), (width/2+135, height-105)]
    for i in range(3):
        draw_h_rect(win, mouse, [width/2-250+i*175, height-100, 150, 50], (0,0,0), (250, 205, 50), border = 2)
    draw_text(strings_p, poss_p, pacifico, (0,0,0))
    draw_text(strings, poss, roboto, (0,0,0))

    # Draws exit menu (save options)
def draw_save_menu(win, mouse, selected, savename):
    c = (255, 255, 255) if selected == "Text prompt" else (200, 200, 200)
    pygame.draw.rect(win,c,[0, 150, width, 25])                 # text prompt rect

    # Text data
    strings = ["Do you want to save the game? If yes, select save name: ", savename]
    poss = [(150, 125), (150, 150)]
    draw_text(strings, poss, roboto, (0,0,0))

    # Save and exit buttons
    draw_h_rect(win, mouse, [width/2-300, height-100, 150, 50], (0,0,0), (250, 205, 50), border = 2)
    draw_h_rect(win, mouse, [width/2-75, height-100, 150, 50], (0,0,0), (250, 205, 50), border = 2)
    draw_h_rect(win, mouse, [width/2+150, height-100, 150, 50], (0,0,0), (250, 205, 50), border = 2)
    strings = ["Back", "Save", "Exit"]
    poss = [(width/2 - 260, height-105), (width/2-35, height-105), (width/2+195, height-105)]
    draw_text(strings, poss, pacifico, (0,0,0))

    # Draws endgame screen
def draw_endgame(win, mouse, world):
    strings = [f"Winner: {world.winner}", f"Ended on turn {world.turn}"]
    poss = [(200, 200), (200, 250)]
    draw_text(strings, poss, roboto, (0,0,0))

    # Main menu button
    draw_h_rect(win, mouse, [width/2-75, height-100, 150, 50], (0,0,0), (250, 205, 50), border = 2)
    strings_p = ["Main Menu"]
    poss_p = [(width/2-55, height-105)]
    draw_text(strings_p, poss_p, pacifico, (0,0,0))



# Updates display (GUI)
def redraw_window(win, view, mouse, world, selected, city, topleft, task, err, page, username, text, player, savename):
    if view == "Start menu":
        win.fill((255, 255, 255))
        draw_start_menu(win, mouse)
        draw_actions(win, selected, view)
    elif view == "Load game":
        win.fill((250,250,210))
        draw_load_menu(win, mouse, page)
    elif view == "SP setup":
        win.fill((250,250,210))
        draw_sp_settings(win, mouse, err, username, text, selected)
    elif view == "Reports main": 
        win.fill((255,0,0))
        draw_reports(win, mouse, city)
        draw_bottom_menu(win, mouse, (255, 100, 100))
        draw_next_turn_button(win, mouse, (255, 100, 100))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "City":
        win.fill((50,204,73))
        if task != None:
            draw_costs(task, city)
            if task.type == "Train":
                draw_training_menu(win, mouse, task, err)
            if task.type == "Build":
                draw_building_menu(win, mouse, task, err, page, city)
            if task.type == "Upgrade":
                draw_text([err], [(width-210, 570)], roboto, (255, 0, 0))
        draw_res(win, city)
        draw_city(win, mouse, city)
        draw_tasks(win, mouse, city)
        draw_points(city)
        draw_bottom_menu(win, mouse, (100, 255, 100))
        draw_next_turn_button(win, mouse, (100, 255, 100))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "Map":
        win.fill((0,0,255))
        draw_map(win, mouse, world, player, topleft)
        draw_map_move_buttons(win, mouse)
        draw_city_info(win, selected)
        draw_bottom_menu(win, mouse, (100, 100, 255))
        draw_next_turn_button(win, mouse, (100, 100, 255))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "Overview":
        win.fill((100, 100, 100))
        draw_overview(win, mouse, player, page)
        draw_bottom_menu(win, mouse, (150, 150, 150))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "Report":
        win.fill((255,0,0))
        draw_full_report(win, mouse, selected)
        draw_bottom_menu(win, mouse, (255, 100, 100))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "Troop select":
        win.fill((0,0,255))
        draw_attack_menu(win, mouse, city, task)
        draw_tasks(win, mouse, city)
        draw_bottom_menu(win, mouse, (100, 100, 255))
        draw_actions(win, selected, view)
        draw_current_turn(win, world.turn)
    elif view == "Save menu":
        win.fill((100, 100, 100))
        draw_save_menu(win, mouse, selected, savename)
        pass
    elif view == "Game Over":
        win.fill((100, 100, 100))
        draw_endgame(win, mouse, world)
    draw_top_menu(win, mouse)
    pygame.display.update()



# Main function
def main():
    world, player, city, topleft, selected, task, savename = None, None, None, None, None, None, "foo"
    run = True
    clock = pygame.time.Clock()
    view = "Start menu"
    err, text, username = "", "", "John Doe"
    num = 0
    page = 0

    while run:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        redraw_window(win, view, mouse, world, selected, city, topleft, task, err, page, username, num, player, savename)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if selected == "Text prompt":
                if view == "SP setup":
                    username = text_prompt(username, event)
                elif view == "Save menu":
                    savename = text_prompt(savename, event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Changing view / quitting
                if view != "Start menu" and view != "SP setup" and view != "Load game":               # Can't change views if no game is running!
                    if width-100 <= mouse[0] <= width and 0 <= mouse[1] <= 25:
                        view = "Save menu"
                        selected, task, err, page = None, None, "", 0
                    elif width-200 <= mouse[0] <= width-100 and 0 <= mouse[1] <= 25:
                        view = "Reports main"
                        selected, task, err, page = None, None, "", 0
                    elif width-300 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 25:
                        view = "City"
                        selected, task, err, page = None, None, "", 0
                    elif width-400 <= mouse[0] <= width-300 and 0 <= mouse[1] <= 25:
                        topleft = city.topleft_coords(world.size)
                        view = "Map"
                        selected, task, err, page = None, None, "", 0
                    elif width-500 <= mouse[0] <= width-400 and 0 <= mouse[1] <= 25:
                        view = "Overview"
                        selected, task, err, page = None, None, "", 0

                # Next turn
                if view in ["Map", "Reports main", "City"] and 23 <= mouse[0] <= 227 and 580 <= mouse[1] <= 630 and event.button == 1:
                    world.next_turn()
                    if world.winner != None:
                        view = "Game Over"
                    else:
                        selected, task, err = None, None, ""
                        view = "City"

                if isinstance(selected, str) and view == "Load game":
                    if width/2-75 <= mouse[0] <= width/2 +75 and height-100 <= mouse[1] <= height-50:
                        with open(f"saves/{selected}", "rb") as f:
                            savename = selected
                            world = pickle.load(f)
                            player = world.players[0]
                            city = player.cities[0]
                            page = 0
                        view = "City"
                    elif width/2+100 <= mouse[0] <= width/2+250 and height-100 <= mouse[1] <= height-50:                                ###############
                        remove(f"saves/{selected}")
                        selected = None

                # Main menu actions
                elif isinstance(selected, Report):
                    if view == "Reports main":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = "Report"
                            selected.read = True
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            city.reports.remove(selected)
                            selected = None
                        elif width/2 <= mouse[0] <= width/2+150 and height-100 <= mouse[1] <= height-50:            # Menu button 3
                            selected.read = True
                    elif view == "Report":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = "Reports main"
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            view = "Reports main"
                            city.reports.remove(selected)
                            selected = None
                
                elif isinstance(selected, City):
                    if view == "Map":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            view = "Troop select"
                            task = Task("Move Troops", [Army([0,0,0,0,0]), city, selected, "Attack"], 2)                                       # Change end turn calculation
                        elif width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:            # Menu button 2
                            view = "Troop select"
                            task = Task("Move Troops", [Army([0,0,0,0,0]), city, selected, "Raid"], 2)                                       # Change end turn calculation
                        elif width/2 <= mouse[0] <= width/2+150 and height-100 <= mouse[1] <= height-50:            # Menu button 3
                            view = "Troop select"
                            task = Task("Move Troops", [Army([0,0,0,0,0]), city, selected, "Espionage"], 2)                                       # Change end turn calculation
                        elif width/2+150 <= mouse[0] <= width/2+300 and height-100 <= mouse[1] <= height-50:        # Menu button 4
                            view = "Troop select"
                            task = Task("Move Troops", [Army([0,0,0,0,0]), city, selected, "Conquest"], 2)                                       # Change end turn calculation
                    elif view == "Troop select":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:
                            city.update_task_endturn(task, world.turn)
                            city.current_tasks.append(task)
                            city.army -= task.data[0]
                            selected, task, err = None, None, ""
                            view = "City"
                    elif view == "Overview":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:
                            city = selected
                            view = "City"
                            selected, task, err, page = None, None, "", 0

                elif isinstance(selected, Building):
                    # Train option
                    if selected.type in ["Training Camp", "Factory", "Range", "Military HQ", "Agency"]:
                        helper_dict = {"Training Camp": "Infantryman", "Range": "Sniper", "Factory": "Tank", "Agency": "Spy", "Military HQ": "General"}
                        if width/2-150 <= mouse[0] <= width/2 and height-100 <= mouse[1] <= height-50:              # Menu button 2
                            task = Task("Train", [helper_dict[selected.type], 0], 2)
                    # Build option
                    if selected.type == "Empty":
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            page = 0
                            task = Task("Build", ["Empty", selected.slot], 2)
                    
                    # Upgrade option
                    elif selected.level < 5:
                        if width/2-300 <= mouse[0] <= width/2-150 and height-100 <= mouse[1] <= height-50:          # Menu button 1
                            task = Task("Upgrade", [selected.type], 2)
                            res, err = city.required_res(task), ""
                            if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:  # Not enough res
                                err = "Need more resources!"
                            elif len(city.current_tasks) == 3:                                                      # Too many tasks
                                err = "Too many tasks!"
                            else:
                                city.update_task_endturn(task, world.turn)
                                city.current_tasks.append(task)
                                city.spend_res(res)
                                selected, task, err = None, None, ""
                            
            
                # View-specific actions
                if view == "Start menu":
                    if width/2-172 <= mouse[0] <= width/2+172 and height/2-152 <= mouse[1] <= height/2-48:
                        view = "SP setup"
                    elif width/2-172 <= mouse[0] <= width/2+172 and height/2-42 <= mouse[1] <= height/2+62:
                        # Multiplayer settings page -- later
                        pass
                    elif width/2-172 <= mouse[0] <= width/2+172 and height/2+68 <= mouse[1] <= height/2+172:
                        view = "Load game"
                    elif width/2-172 <= mouse[0] <= width/2+172 and height/2+178 <= mouse[1] <= height/2+282:
                        run = False
                        pygame.quit()

                elif view == "Reports main":
                    for i in range(min(8, len(city.reports))):
                        if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+i*50 <= mouse[1] <= height/2-227+i*50:
                            selected, task = city.reports[i], None
                
                # Singleplayer game setup
                elif view == "SP setup":
                    if 150 <= mouse[1] <= 175:
                        selected = "Text prompt"
                    elif 200 <= mouse[0] <= 240 and 250 <= mouse[1] <= 290:
                        num = max(0, num - 1)
                    elif 250 <= mouse[0] <= 290 and 250 <= mouse[1] <= 290:
                        num = min(9, num + 1)
                    elif width/2 - 100 <= mouse[0] <= width/2 + 100 and 450 < mouse[1] < 550:
                        players = [Player(username, [])]
                        players += [Player(f"AI {i}", []) for i in range(num)]
                        npc_count = len(players)*6
                        npcs = [Player(f"NPC {i}", []) for i in range(npc_count)]
                        world = World(players)
                        world.players += npcs
                        world.start_game()
                        player = world.players[0]
                        city = player.cities[0]
                        topleft = city.topleft_coords(world.size)
                        view = "City"
                    else:
                        selected = None

                # City view actions
                elif view == "City":

                    # Task cancel
                    h = 83
                    for i in range(len(city.current_tasks)):
                        if 199 <= mouse[0] <= 219 and h <= mouse[1] <= h+20:
                            temp = city.current_tasks[i]
                            res = city.required_res(temp)
                            city.add_res(res)
                            city.current_tasks.pop(i)
                            break
                        h += 10 + 20*len(str(city.current_tasks[i]).split("\n"))

                    # Building selection
                    if city.size == 6:
                        x, y = (3, 2)
                        for i in range(x):
                            for j in range(y):
                                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-180+j*150 <= mouse[1] <= height/2-30+j*150:
                                    selected, task, err = city.buildings[3*j + i + 1], Task("Upgrade", [city.buildings[3*j + i + 1].type]), ""
                    elif city.size == 9:
                        x, y = (3, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-225+i*150 <= mouse[0] <= width/2-75+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task, err = city.buildings[3*j + i + 1], Task("Upgrade", [city.buildings[3*j + i + 1].type]), ""
                    elif city.size == 12:
                        x, y = (4, 3)
                        for i in range(x):
                            for j in range(y):
                                if width/2-300+i*150 <= mouse[0] <= width/2-150+i*150 and height/2-255+j*150 <= mouse[1] <= height/2-105+j*150:
                                    selected, task, err = city.buildings[4*j + i + 1], Task("Upgrade", [city.buildings[4*j + i + 1].type]), ""
                    # Select Wall
                    if width/2-300 <= mouse[0] <= width/2+300 and height/2+195 <= mouse[1] <= height/2+220:
                        selected, task, err = city.buildings[0], Task("Upgrade", [city.buildings[0].type]), ""
                    
                    
                    # Right menu actions
                    if task != None:
                        # Training
                        if task.type == "Train":
                            err = ""
                            if width-187 <= mouse[0] <= width-137 and 270 <= mouse[1] <= 320:
                                if task.data[1] - 1 >= 0:
                                    task.data[1] -= 1
                                    err = ""
                            if width-117 <= mouse[0] <= width-67 and 270 <= mouse[1] <= 320:
                                task.data[1] += 1
                                res, err = city.required_res(task), ""
                                if task.data[1] > city.calc_housing():
                                    err = "Not enough space!" 
                                    task.data[1] -= 1
                                elif res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                    err = "Need more resources!"
                                    task.data[1] -= 1
                            if width-187 <= mouse[0] <= width-137 and 330 <= mouse[1] <= 380:
                                if task.data[1] - 10 >= 0:
                                    task.data[1] -= 10
                            if width-117 <= mouse[0] <= width-67 and 330 <= mouse[1] <= 380:
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
                                elif len(city.current_tasks) == 3:
                                    err = "Too many tasks!"
                                elif task.data[1] == 0:
                                    err = "Select more units!"
                                else:
                                    res = city.required_res(task)
                                    city.update_task_endturn(task, world.turn)
                                    city.current_tasks.append(task)
                                    city.spend_res(res)
                                    selected, task, err = None, None, ""
                        
                        # Building
                        elif task.type == "Build":

                            # Building selection
                            for i, b in enumerate(building_costs):
                                if i in range(8*(page), 8*(page+1)):
                                    if width-205 <= mouse[0] <= width-45 and 205+27*(i%8) <= mouse[1] <= 230+27*(i%8):
                                        task.data[0], err = b, ""
                            
                            # Prev/Next button
                            if width-195 <= mouse[0] <= width-137 and 470 <= mouse[1] <= 495:
                                page, err = max(page-1, 0), ""
                            if width-125 <= mouse[0] <= width-67 and 470 <= mouse[1] <= 495:
                                page, err = min(page+1, ceil(len(values.building_costs)/8)-1), ""

                            # Confirmation
                            if width-202 <= mouse[0] <= width-52 and 500 <= mouse[1] <= 550:
                                if task.data[0] == "Empty":
                                    err = "Select building!"
                                elif task in city.current_tasks:
                                    err = "Already started!"
                                elif task.data[0] in [b.type for b in list(city.buildings.values())]:
                                    err = "Already built!"
                                elif task.data[1] == 0 and task.data[0] != "Wall":
                                    err = "Slot reserved for wall!"
                                elif task.data[1] != 0 and task.data[0] == "Wall":
                                    err = "Can't build wall here!"
                                else:
                                    res, err = city.required_res(task), ""
                                    if res[0] > city.resources[0] or res[1] > city.resources[1] or res[2] > city.resources[2]:
                                        err = "Need more resources!"
                                    elif len(city.current_tasks) == 3:
                                        err = "Too many tasks!"
                                    else:
                                        city.update_task_endturn(task, world.turn)
                                        city.current_tasks.append(task)
                                        city.spend_res(res)
                                        selected, task, err, page = None, None, "", 0

                # Map view actions
                elif view == "Map":
                    # Selecting a city:
                    x, y = (7, 5)
                    for i in range(x):
                        for j in range(y):
                            if width/2-350+i*100 <= mouse[0] <= width/2-250+i*100 and height/2-280+j*100 <= mouse[1] <= height/2-180+j*100:
                                if world.map[(topleft[0]+i,topleft[1]+j)] not in [f"Empty{i}" for i in range(1,5)]:
                                    selected = world.map[(topleft[0]+i,topleft[1]+j)]
                    # Map movement
                    if width-150 <= mouse[0] <= width-100 and height-202 <= mouse[1] <= height-152:
                        if topleft[1] > -world.size:
                            topleft = (topleft[0], topleft[1] - 1)
                    elif width-150 <= mouse[0] <= width-100 and height-98 <= mouse[1] <= height-48:    
                        if topleft[1] < world.size-4:
                            topleft = (topleft[0], topleft[1] + 1)
                    elif width-202 <= mouse[0] <= width-152 and height-150 <= mouse[1] <= height-100:
                        if topleft[0] > -world.size:
                            topleft = (topleft[0]-1, topleft[1])
                    elif width-98 <= mouse[0] <= width-48 and height-150 <= mouse[1] <= height-100:
                        if topleft[0] < world.size - 6:
                            topleft = (topleft[0]+1, topleft[1])

                # Troop movement menu actions
                elif view == "Troop select":
                    # Unit selection
                    for i, unit in enumerate(Army().units): # For each line
                        for change, j in zip([-1, -task.data[0].units[unit], 1, 10, 100, city.army.units[unit]], range(6)): # for each column
                            if width/2-102+j*70 <= mouse[0] <= width/2-48+j*70 and height/2-247+95*i <= mouse[1] <= height/2-193+95*i: # If clicked
                                if 0 <= task.data[0].units[unit] + change <= city.army.units[unit]:    # If enough troops and not going below 0
                                    task.data[0].units[unit] += change         # Add troops 

                # Overview menu actions
                elif view == "Overview":
                    for i, city in enumerate(player.cities):
                        if i in range(8*(page), 8*(page+1)):
                            if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+52*(i%8) <= mouse[1] <= height/2-227+52*(i%8):
                                selected, err = player.cities[i], ""
                    if len(player.cities) > 8:
                        if width/2-100 <= mouse[0] <= width/2-20 and 500 <= mouse[1] <= 540:
                            page = max(page-1, 0)
                        elif width/2+20 <= mouse[0] <= width/2+100 and 500 <= mouse[1] <= 540:
                            page = min(page+1, ceil(len(player.cities)/8)-1)

                elif view == "Load game":
                    saves = saves_list()
                    for i, save in enumerate(saves):
                        if i in range(8*(page), 8*(page+1)):
                            if width/2-347 <= mouse[0] <= width/2+347 and height/2-277+52*(i%8) <= mouse[1] <= height/2-227+52*(i%8):
                                selected, err = save, ""
                    if len(saves) > 8:
                        if width/2-100 <= mouse[0] <= width/2-20 and 500 <= mouse[1] <= 540:
                            page = max(page-1, 0)
                        elif width/2+20 <= mouse[0] <= width/2+100 and 500 <= mouse[1] <= 540:
                            page = min(page+1, ceil(len(saves)/8)-1)
                    if width/2-250 <= mouse[0] <= width/2-100 and height-100 <= mouse[1] <= height-50:
                        view = "Start menu"
                        selected, page = None, 0

                elif view == "Save menu":
                    if 150 <= mouse[1] <= 175:
                        selected = "Text prompt"
                    else: 
                        selected = None
                    if width/2-300 <= mouse[0] <= width/2+150 and  height-100 <= mouse[1] <= height-50:
                        view = "City"
                    elif width/2-75 <= mouse[0] <= width/2+75 and  height-100 <= mouse[1] <= height-50:
                        with open(f"saves/{savename}", "wb") as file:
                            pickle.dump(world, file)
                        err = "Saved!"
                    elif width/2+150 <= mouse[0] <= width/2+300 and  height-100 <= mouse[1] <= height-50:
                        view = "Start menu"
                        world, player, city, topleft, selected, task, savename, err = None, None, None, None, None, None, "", ""
                    else:
                        err = ""
                elif view == "Game Over":
                    if width/2-75 <= mouse[0] <= width/2+75 and  height-100 <= mouse[1] <= height-50:
                        view = "Start Menu"


main()
