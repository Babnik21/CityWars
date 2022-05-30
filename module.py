from random import choice, shuffle, uniform, choices, randint
from math import floor, ceil, sqrt, e
import values
import re
import numpy as np
import copy
import pickle

class World():
    def __init__(self, players):
        self.players = players
        self.size = 2 + len(self.players)
        self.cities = []
        self.turn = 1
        self.win_con = 1000
        self.winner = None
        lst = []
        for i in range(-self.size, self.size+1):
            for j in range(-self.size, self.size+1):
                lst.append((i,j))
        self.empty_coords = lst
        self.map = {}
        for key in self.empty_coords:
            self.map[key] = f"Empty{choice([1,2,3,4])}"

    def __repr__(self):
        return f"World of size {self.size*2+1}x{self.size*2+1} with {len(self.cities)} cities. Current turn: {self.turn}"

    def start_game(self):
        names = values.cities
        shuffle(names)
        for p, name in zip(self.players, names):
            if re.match("^NPC\s\d+$", p.username):
                self.spawn_city(p, choices([6, 9, 12], weights=[0.2, 0.4, 0.4])[0], name)
            else:
                self.spawn_city(p, 12, name)
        self.win_con = len(self.players)//2 + 1

    #Adds a new city on the map (returns coords for now)
    def spawn_city(self, player, size, name):
        coords = choice(self.empty_coords)
        city = City(player, size, coords, [], name)
        player.add(city)
        self.cities.append(city)
        self.empty_coords.remove(coords)
        self.map[coords] = city
        return coords

    def game_over(self):
        for p in self.players:
            if len(p.cities) >= self.win_con:
                self.winner = p.username

    def next_turn(self):
        shuffle(self.cities)
        for city in self.cities:
            city.update_powers()
            if re.match("^NPC\s\d+$", city.owner.username):
                npc_move(city, self.turn)
            elif re.match("^AI\s\d+$", city.owner.username):
                ai_move(city, self)
            city.ongoing_tasks += city.current_tasks
            city.current_tasks = []
            delete = []
            city.ongoing_tasks.sort()
            for task in city.ongoing_tasks:
                if task.end_turn == self.turn + 1:
                    city.execute(task, self.turn)
                    delete.append(task)
            city.update_res()
            city.ongoing_tasks = [item for item in city.ongoing_tasks if item not in delete]
            city.reports.sort()
        self.turn += 1
        self.game_over()
        print(f"Starting turn {self.turn}")

class Player():
    def __init__(self, username, cities=[]):
        self.username = username
        self.cities = cities
        if re.match("^NPC\s\d+$", self.username):
            self.color = (210, 105, 30)
        elif re.match("^AI\s\d+$", self.username):
            self.color = values.colors[int(self.username[-1])]
        else:
            self.color = (0, 0, 0)

    def __str__(self):
        return self.username
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        else:
            return False

    def add(self, city):
        self.cities.append(city)

class City():
    def __init__(self, owner, size, coords, reports, name):
        self.owner = owner
        self.size = size
        self.coords = coords
        self.buildings = {}
        self.points = 1
        self.powers = 0
        for i in range(size+1):
            self.buildings[i] = Building(slot=i)
        self.army = Army()
        self.resources = [150, 150, 5]
        self.current_tasks = []
        self.ongoing_tasks = []
        self.reports = reports
        self.name = name
        self.update_powers()

    def buildings_to_str(self):
        string = ""
        for key in self.buildings.keys():
            string += str(self.buildings[key])
        return string

    def __repr__(self):
        return f"{self.name} owned by {self.owner} at {self.coords}. \nArmy: \n" + str(self.army) + "\nBuildings: \n" + self.buildings_to_str()

    def __str__(self):
        return f"{self.name} owned by {self.owner} at {self.coords}. \nArmy: \n" + str(self.army) + "\nBuildings: \n" + self.buildings_to_str()

    def __eq__(self, other):
        if isinstance(other, City):
            return self.coords == other.coords
        else:
            return False

    def train(self, units, num):
        self.army.train(units, num)

    def build(self, b, slot):
        self.buildings[slot] = Building(b, 1, slot)
        self.points += values.points[b][1]

    def find_slot(self, building):
        for s in self.buildings:
            if self.buildings[s].type == building:
                return s
        return None

    def find_level(self, building):
        for b in self.buildings:
            if self.buildings[b].type == building:
                return self.buildings[b].level
        return 0

    # Finds topleft coords for map viewing
    def topleft_coords(self, worldsize):
        coords = [self.coords[0]-3, self.coords[1]-2]
        if coords[0] + 6 > worldsize:
            coords[0] = worldsize - 6
        elif coords[0] < -worldsize:
            coords[0] = -worldsize
        if coords[1] > worldsize - 4:
            coords[1] = worldsize - 4
        elif coords[1] < -worldsize:
            coords[1] = -worldsize
        return coords

    # Upgrades selected building in city
    def upgrade(self, b):
        slot = self.find_slot(b)
        type = self.buildings[slot].type
        lvl = self.buildings[slot].level
        self.buildings[slot] = Building(type, lvl+1, slot)
        self.points += values.points[b][lvl+1]

    # Calculates remaining housing space
    def calc_housing(self):
        troops = self.army.count()
        for task in self.current_tasks + self.ongoing_tasks:
            if task.type == "Train":
                troops += task.data[1]
        return values.housing_capacity[self.find_level("Housing")] - troops

    # Main method for executing tasks
    def execute(self, task, curr_turn):
        if task.type == "Build":
            self.build(task.data[0], task.data[1])
        elif task.type == "Upgrade":
            self.upgrade(task.data[0])
        elif task.type == "Move Troops":            
            # If returning from combat:
            if task.data[3] == "Return":
                self.army += task.data[0]                   # Adds returning army to current army and kills units there's no room for
                self.army.fit_housing(values.housing_capacity[self.find_level("Housing")])
                self.add_res(task.data[4])                  # Adds looted resources

            # If NOT returning from combat
            else:
                result = self.combat_calculation(task)      # Calculate combat results
                r_army = task.data[0] - result[0]           # Atk surviving army
                self.make_report(task, result)              # Make reports
                task.data[2].army -= result[1]              # Kill defending units
                if task.data[3] == "Conquest" and result[4]:
                    loser = task.data[2].owner              # If conquered, change village owner
                    loser.cities.remove(task.data[2])
                    task.data[2].owner = self.owner
                    self.owner.cities.append(task.data[2])

                # Make new task for troop return
                if r_army != 0:
                    self.ongoing_tasks.append(Task("Move Troops", [r_army, task.data[2], self, "Return", result[5]], 2))   # Change end turn !!!!
                    self.update_task_endturn(self.ongoing_tasks[-1], curr_turn + 1)
        elif task.type == "Train":
            self.army.units[task.data[0]] += task.data[1]

    # Updates attack and defense power
    def update_powers(self):
        atk = self.army.power("A", 0, 0)
        deff = self.army.power("D", 0, self.find_level("Wall"))
        self.powers = (atk, deff)

    # Produces resources
    def update_res(self):

        # Add values
        food = values.farm_prod[self.find_level("Farm")] + values.bakery_prod[self.find_level("Bakery")]
        iron = values.iron_prod[self.find_level("Iron Mine")]
        gold = values.gold_prod[self.find_level("Gold Mine")]
        # Avoid overflow
        food = min(food, values.warehouse_capacity[self.find_level("Warehouse")] - self.resources[0])
        iron = min(iron, values.warehouse_capacity[self.find_level("Warehouse")] - self.resources[1])
        gold = min(gold, values.bank_capacity[self.find_level("Bank")] - self.resources[2])
        # Update
        self.resources = [self.resources[0] + food, self.resources[1] + iron, self.resources[2] + gold]

    # Spends resources
    def spend_res(self, res):
        self.resources = [self.resources[0] - res[0], self.resources[1] - res[1], self.resources[2] - res[2]]

    # Adds resources
    def add_res(self, res):
        self.resources = [self.resources[0] + res[0], self.resources[1] + res[1], self.resources[2] + res[2]]

    # Returns loot and removes res form def village (for now)
    def steal_res(self, cap):
        if self.resources[0]+self.resources[1] == 0:
            available_f = 0
            available_i = 0
        else:
            ratio_f_1 = self.resources[0]/(self.resources[0]+self.resources[1])
            ratio_i_1 = self.resources[1]/(self.resources[0]+self.resources[1])
            available_f = max(0, self.resources[0] - floor(values.bunker_capacity[self.find_level("Bunker")]*ratio_f_1))
            available_i = max(0, self.resources[1] - floor(values.bunker_capacity[self.find_level("Bunker")]*ratio_i_1))
        available_g = max(0, self.resources[2] - values.vault_capacity[self.find_level("Vault")])
        if available_g + available_f + available_i <= cap:
            loot = [available_f, available_i, available_g]
        else:
            ratio_f = available_f/(available_f+available_i+available_g)
            ratio_i = available_i/(available_f+available_i+available_g)
            ratio_g = available_g/(available_f+available_i+available_g)
            loot = [floor(cap*ratio_f), floor(cap*ratio_i), floor(cap*ratio_g)]
        self.spend_res(loot)
        return loot

    # Returns amount of resources required to start selected task (works for task or list of tasks)
    def required_res(self, task):
        if isinstance(task, Task):
            if task.type == "Build" or task.type == "Upgrade":
                lvl = self.find_level(task.data[0])
                return values.building_costs[task.data[0]][lvl]
            elif task.type == "Train":
                return [task.data[1] * x for x in values.unit_costs[task.data[0]]]
            else: 
                return [0,0,0]
        else:
            res = [0,0,0]
            for t in task:
                if t != None:
                    if t.type == "Build" or t.type == "Upgrade":
                        lvl = self.find_level(t.data[0])
                        cost = values.building_costs[t.data[0]][lvl]
                        res = [res[0]+cost[0], res[1]+cost[1], res[2]+cost[2]] 
                    elif t.type == "Train":
                        cost = [t.data[1] * x for x in values.unit_costs[t.data[0]]]
                        res = [res[0]+cost[0], res[1]+cost[1], res[2]+cost[2]]
            return res

    # Returns true if there are enough resources available else false
    def enough_res(self, res):
        return self.resources[0] >= res[0] and self.resources[1] >= res[1] and self.resources[2] >= res[2]

    # Main function for calculating combat results --> returns (a_dead, d_dead, luck, bool_spotted, bool_conquered)
    def combat_calculation(self, task):
        luck = uniform(-0.1, 0.1)
        wall = task.data[2].find_level("Wall")
        conq = False
        a_pow = task.data[0].power("A", luck, wall)
        d_pow = task.data[2].army.power("D", luck, wall)
        if task.data[3] == "Raid":
            rate = a_pow/(a_pow + d_pow)
            d_dead = task.data[2].army * rate
            a_dead = task.data[0] * (1-rate)
            r_army = task.data[0] - a_dead           # Atk surviving army
            cap = r_army.capacity()                 # Calculate carrying capacity
            loot = task.data[2].steal_res(cap)      # Remove loot from defending city
            return a_dead, d_dead, luck, True, conq, loot
        elif task.data[3] == "Espionage":
            if task.data[2].army.units["Spy"] == 0:
                return Army([0,0,0,0,0]), Army([0,0,0,0,0]), luck, False, False, [0,0,0]
            else:
                a_spies = task.data[0].units["Spy"]
                d_spies = task.data[2].army.units["Spy"]
                a_dead = Army([0,0,0,min(a_spies, ceil(d_spies/((1+luck)*1.2))),0])
                return a_dead, Army([0,0,0,0,0]), luck, True, conq, [0,0,0]
        else:
            if a_pow >= d_pow:
                rate = d_pow / a_pow
                d_dead = task.data[2].army
                a_dead = task.data[0] * rate
            else: 
                rate = a_pow/d_pow
                a_dead = task.data[0]
                d_dead = task.data[2].army * rate
            if task.data[3] == "Conquest" and task.data[0].units["General"] > a_dead.units["General"]:
                conq = True
            return a_dead, d_dead, luck, True, conq, [0,0,0]

    # Adds report to attacker village's reports and returns defender report to be manually appended to its reports (if not, returns None)
    def make_report(self, task, combat_calc):
        a_city = task.data[1]
        d_city = task.data[2]
        turn = task.end_turn
        type = task.data[3]
        a_army = task.data[0]
        d_army = task.data[2].army
        a_dead = combat_calc[0]
        d_dead = combat_calc[1]
        luck = combat_calc[2]
        spotted = combat_calc[3]
        conq = combat_calc[4]
        loot = combat_calc[5]
        r_atk = Report(a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, loot, conq)
        r_def = Report(a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, loot, conq)
        self.reports.append(r_atk)
        if spotted:
            d_city.reports.append(r_def)

    # Updates task endturn
    def update_task_endturn(self, task, curr_turn):
        if task.type == "Build" or task.type == "Upgrade":
            task.end_turn = curr_turn + 1
        elif task.type == "Train":
            b = values.unit_training_place[task.data[0]]
            task.end_turn = curr_turn + values.training_spd[b][self.find_level(b)]
        elif task.type == "Move Troops":
            dist = distance(task.data[1], task.data[2])
            duration = max(dist/values.unit_stats[key][2] for key in task.data[0].units if task.data[0].units[key] > 0)     # Determined by slowest unit
            task.end_turn = curr_turn + ceil(duration)

class Task():
    def __init__(self, type=None, data=None, end_turn=None):
        self.type = type
        self.data = data
        self.end_turn = end_turn

    def __str__(self):
        if self.type == "Train":
            return f"Train {self.data[1]} x {self.data[0]}.\nCompleted: turn {self.end_turn}."
        elif self.type == "Move Troops":
            if self.data[3] == "Return":
                return f"Return from {self.data[1].coords} \nReturning army:\n{self.data[0]}.\nCompleted: turn {self.end_turn}"
            else: 
                return f"{self.data[3]}: {self.data[2].coords}\nArmy: \n{self.data[0]}\nCompleted: turn {self.end_turn}"
        else:
            return f"{self.type} {self.data[0]}. \nCompleted: turn {self.end_turn}"

    def __repr__(self):
        if self.type == "Move Troops":
            return f"Task({self.type}, {self.data}, type {self.data[3]}, {self.end_turn})"
        else:
            return f"Task({self.type}, {self.data}, {self.end_turn})"

    def __eq__(self, other):
        if isinstance(other, Task):
            if self.type == "Build" and other.type == "Build":
                return self.data[0]==other.data[0] or self.data[1] == other.data[1]
            elif self.type == "Upgrade":
                return self.data[0] == other.data[0] and self.type == other.type
            elif self.type == "Train":
                return self.data[0] == other.data[0] and self.type == other.type and self.end_turn == other.end_turn
        return False

    def __lt__(self, other):
        return self.end_turn < other.end_turn

    def housing_req(self):
        if self.type == "Train":
            return self.data[1]
        else:
            return 0

class Report():
    def __init__(self, a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, loot, conq = False, read = False):
        self.turn = turn
        self.a_city = a_city
        self.d_city = d_city
        self.a_army = a_army
        self.d_army = d_army
        self.a_dead = a_dead
        self.d_dead = d_dead
        self.luck = luck
        self.type = type
        self.read = read
        self.conq = conq
        self.loot = loot
        
    def __repr__(self):
        return f"{self.type} on {self.d_city.coords}, turn {self.turn}."

    def __str__(self):
        headline = f"{self.type} by {self.a_city.name} {self.a_city.coords} on {self.d_city.name} ({self.d_city.coords}), turn {self.turn}."
        if not self.read:
            headline = "UNREAD -- " + headline
        a_army = f"Attacking army: \nInfantryman: {self.a_army.units['Infantryman']}\nSniper: {self.a_army.units['Sniper']}\nTank: {self.a_army.units['Tank']}\nSpy: {self.a_army.units['Spy']}\nGeneral: {self.a_army.units['General']}."
        a_dead = f"Casualties: \nInfantryman: {self.a_dead.units['Infantryman']}\nSniper: {self.a_dead.units['Sniper']}\nTank: {self.a_dead.units['Tank']}\nSpy: {self.a_dead.units['Spy']}\nGeneral: {self.a_dead.units['General']}."
        d_army = f"Defending army: \nInfantryman: {self.d_army.units['Infantryman']}\nSniper: {self.d_army.units['Sniper']}\nTank: {self.d_army.units['Tank']}\nSpy: {self.d_army.units['Spy']}\nGeneral: {self.d_army.units['General']}."
        d_dead = f"Casualties: \nInfantryman: {self.d_dead.units['Infantryman']}\nSniper: {self.d_dead.units['Sniper']}\nTank: {self.d_dead.units['Tank']}\nSpy: {self.d_dead.units['Spy']}\nGeneral: {self.d_dead.units['General']}."
        if self.luck > 0:
            luck = f"Attackers were lucky ({round(self.luck*100, 2)}% bonus power)."
        else:
            luck = f"Attackers were unlucky ({round(-self.luck*100, 2)}% power deduction)."
        loot = f"Attackers were able to steal {self.loot[0]} food, {self.loot[1]} iron and {self.loot[2]} gold."
        conq = "The city has been conquered." if self.conq else "The city has not been conquered."
        return headline + a_army + a_dead + d_army + d_dead + luck + loot + conq

    def __lt__(self, other):
        return self.turn > other.turn

class Army():
    def __init__(self, units = [0,0,0,0,0]):
        self.units = {
            "Infantryman": units[0],
            "Sniper": units[1],
            "Tank": units[2],
            "Spy": units[3],
            "General": units[4]
        }

    def __eq__(self, other):
        if isinstance(other, Army):
            return self.units == other.units
        elif isinstance(other, int):
            for key in self.units:
                if self.units[key] != other:
                    return False
            return True

    def __add__(self, other):
        return Army([self.units["Infantryman"]+other.units["Infantryman"],
                        self.units["Sniper"]+other.units["Sniper"],
                        self.units["Tank"]+other.units["Tank"],
                        self.units["Spy"]+other.units["Spy"],
                        self.units["General"]+other.units["General"]])

    def __sub__(self, other):
        return Army([self.units["Infantryman"]-other.units["Infantryman"],
                        self.units["Sniper"]-other.units["Sniper"],
                        self.units["Tank"]-other.units["Tank"],
                        self.units["Spy"]-other.units["Spy"],
                        self.units["General"]-other.units["General"]])

    def __mul__(self, other):
        infantryman = ceil(self.units["Infantryman"] * other)
        sniper = ceil(self.units["Sniper"] * other)
        tank = ceil(self.units["Tank"] * other)
        spy = ceil(self.units["Spy"] * other)
        general = round(self.units["General"] * other)
        return Army([infantryman, sniper, tank, spy, general])

    def __contains__(self, other):
        return self.units["Infantryman"] >= other.units["Infantryman"] and \
            self.units["Sniper"] >= other.units["Sniper"] and \
            self.units["Tank"] >= other.units["Tank"] and \
            self.units["Spy"] >= other.units["Spy"] and \
            self.units["General"] >= other.units["General"]

    def __repr__(self):
        return f"Infantryman: {self.units['Infantryman']},\nSniper: {self.units['Sniper']},\nTank: {self.units['Tank']},\nSpy: {self.units['Spy']},\nGeneral: {self.units['General']}"

    def __str__(self):
        return f"Infantryman: {self.units['Infantryman']},\nSniper: {self.units['Sniper']},\nTank: {self.units['Tank']},\nSpy: {self.units['Spy']},\nGeneral: {self.units['General']}"
    
    def fit_housing(self, space):
        total = self.count()
        if total > space:
            rate = space/total
            for u in self.units:
                self.units[u] = floor(self.units[u]*rate)

    def train(self, unit, num):
        self.units[unit] += num

    def power(self, side, luck, wall):
        power = 0
        if side == "D":
            power += values.wall_power[wall] 
        for u in self.units:
            if side == "A":
                power += self.units[u] * values.unit_stats[u][0] * (1+luck)
            else:
                power += self.units[u] * values.unit_stats[u][1]
        return power

    def capacity(self):
        cap = 0
        for u in self.units:
            cap += self.units[u] * values.unit_stats[u][3]
        return cap

    def count(self):
        return sum(self.units[u] for u in self.units)

class Building():
    def __init__(self, type="Empty", level=0, slot=1):
        self.type = type
        self.level = level
        self.slot = slot
        path = type.lower().replace(" ", "_")
        self.img = f"images/{path}.png"

    def __str__(self):
        return f"{self.type} (lvl {self.level})\n"

    def __repr__(self):
        return f"{self.type} (lvl {self.level})"

    def __eq__(self, other):
        if isinstance(other, Building):
            return self.type == other.type
        else: 
            return False

def distance(c1, c2):
    return sqrt((c1.coords[0] - c2.coords[0])**2 + (c1.coords[1] - c2.coords[1])**2)

# Returns a list of possible tasks.
def possible_tasks_npc(city):
    tasks = []
    building_slots = []
    building_tasks = []
    space = city.calc_housing()
    for b in city.buildings.values():
        if b.level == 0:
            building_slots.append(b.slot)
        elif b.level < 5:
            tasks.append(Task("Upgrade", data=[b.type], end_turn=0))
        if b.type in ["Training Camp", "Range", "Factory", "Agency", "Military HQ"] and re.match("^AI\s\d+$", city.owner.username):
            unit = values.units_trained_in[b.type]
            troop_cost = values.unit_costs[unit]
            if troop_cost[2] == 0:
                max_troops = floor(min([city.resources[0]/troop_cost[0], city.resources[1]/troop_cost[1]]))
            else:
                max_troops = floor(min([city.resources[0]/troop_cost[0], city.resources[1]/troop_cost[1], city.resources[2]/troop_cost[2]]))
            for i in [0.1*max_troops, 0.2*max_troops, 0.5*max_troops, max_troops]:
                task = Task("Train", data = [unit, floor(i)], end_turn=0)
                cost = city.required_res(task)
                if city.enough_res(cost) and space >= i:
                    tasks.append(task)
                else:
                    break

    if 0 in building_slots:
        tasks.append(Task("Build", ["Wall", 0], end_turn=0))
        building_slots.remove(0)
    if len(building_slots) > 0:
        for b in values.building_costs:
            if b != "Wall" and Building(b) not in city.buildings.values():
                building_tasks.append(Task("Build", [b, 1], end_turn=0))

    triples = [[]]
    for i in range(len(building_tasks)):
        if city.enough_res(city.required_res([building_tasks[i]])):
            triples.append([building_tasks[i]])
            if len(building_slots) - 1 > 0:
                for j in range(i+1, len(building_tasks)):
                    if city.enough_res(city.required_res([building_tasks[i], building_tasks[j]])):
                        triples.append([building_tasks[i], building_tasks[j]])
                        if len(building_slots) - 2 > 0:
                            for k in range(j+1, len(building_tasks)):
                                if city.enough_res(city.required_res([building_tasks[i], building_tasks[j], building_tasks[k]])):
                                    triples.append([building_tasks[i], building_tasks[j], building_tasks[k]])
                        for task in tasks:
                            if city.enough_res(city.required_res([building_tasks[i], building_tasks[j], task])):
                                triples.append([building_tasks[i], building_tasks[j], task])
            for j in range(i + 1, len(tasks)):
                if city.enough_res(city.required_res([building_tasks[i], tasks[j]])):
                    triples.append([building_tasks[i], tasks[j]])
                    for k in range(j+1, len(tasks)):
                        if city.enough_res(city.required_res([building_tasks[i], tasks[j], tasks[k]])) and tasks[k] != tasks[j] and tasks[j].housing_req() + tasks[k].housing_req() <= space:
                            triples.append([building_tasks[i], tasks[j], tasks[k]])
    for i in range(len(tasks)):
        if city.enough_res(city.required_res([tasks[i]])):
            triples.append([tasks[i]])
            for j in range(i+1, len(tasks)):
                if city.enough_res(city.required_res([tasks[i], tasks[j]])) and tasks[i] != tasks[j] and tasks[i].housing_req() + tasks[j].housing_req() <= space:
                    triples.append([tasks[i], tasks[j]])
                    for k in range(j+1, len(tasks)):
                        if city.enough_res(city.required_res([tasks[i], tasks[j], tasks[k]])) and tasks[k] != tasks[j] and tasks[i].housing_req() + tasks[j].housing_req() + tasks[k].housing_req() <= space:
                            triples.append([tasks[i], tasks[j], tasks[k]])

    return triples

def update_building_slots(city, tasks):
    slots = [i for i in city.buildings if city.buildings[i].type == "Empty" and i != 0]
    for task in tasks:
        if task.type == "Build":
            if task.data[0] == "Wall":
                slot = 0
            else:
                slot = choice(slots)
            task.data = [task.data[0], slot]

def utility(city, triple, turn):
    copy_1 = copy.deepcopy(city)
    update_building_slots(city, triple)
    for task in triple:
        copy_1.execute(task, turn)
    u = copy_1.points     # Points
    u += (copy_1.resources[0] + copy_1.resources[1])**0.25 + 10*copy_1.resources[2]      # Resources
    u += copy_1.army.power("A", 0, 0)**0.75 + copy_1.army.power("D", 0, copy_1.find_level("Wall"))**0.5     # Army strength
    u += 200*(copy_1.army.units["General"]**0.5)    # General bonus
    u += copy_1.calc_housing()
    if copy_1.army.units["Spy"] > 0:
        u += 100 + 10*(copy_1.army.units["Spy"] ** 0.5)       # Spy bonus
    if copy_1.find_slot("Empty") != None:
        u += 200                                                # Empty building slot bonus
    food = values.farm_prod[copy_1.find_level("Farm")] + values.bakery_prod[copy_1.find_level("Bakery")]
    iron = values.iron_prod[copy_1.find_level("Iron Mine")]
    gold = values.gold_prod[copy_1.find_level("Gold Mine")]
    u += 2.5*(food + iron) + 100*gold
    return u

def attack_seletion(city, world):
    weaker = []
    stronger = []
    for c in world.cities:
        if c.owner.username != city.owner.username and c.owner.username != "Tester":
            if c.powers[1] < city.powers[0] and c.owner.username != world.players[0].username:
                weaker.append(c)
            else:
                stronger.append(c)
    i = randint(1, 50)
    if i%2 == 0 and len(weaker) > 0:
        return max(weaker, key = lambda x: attack_utility(city, x))
    elif i == 1 and len(stronger) > 0:
        return choice(stronger)

def attack_utility(a_city, d_city):
    remaining = simulate_combat(a_city.army, d_city.powers[1])
    u = 0
    if remaining.units["General"] >= 0:
        u += d_city.points + 100000    # Conquest bonus (priority!)
    u += (remaining.power("A", 0, 0) + remaining.power("D", 0, a_city.find_level("Wall")))**0.5     # Remaining army utility
    u += 100/distance(a_city, d_city)       #Distance to city
    u += a_city.army.count()                #Clear housing space bonus
    return u

def simulate_combat(army, d_power):
    a_power = army.power("A", 0, 0)
    if d_power >= a_power:
        return Army([0,0,0,0,0])
    else:
        return army*(1 - d_power/a_power)

def select_ai_move(city, world):
    selected_tasks = []
    tasks_1 = possible_tasks_npc(city)
    attack_target = attack_seletion(city, world)
    if attack_target != None and city.army != 0:
        if city.army.units["General"] > 0:
            selected_tasks.append(Task("Move Troops", [city.army, city, attack_target, "Conquest", ], end_turn = 0))
        else:
            selected_tasks.append(Task("Move Troops", [city.army, city, attack_target, "Raid", ], end_turn = 0))
        tasks_1 = [x for x in tasks_1 if len(x) <= 2]
    sorted_tasks = sorted(tasks_1, key= lambda x: utility(city, x, world.turn), reverse = True)
    weights = [e**(-i) for i in range(1, len(sorted_tasks) + 1)]
    selected_tasks += choices(sorted_tasks, weights)[0]
    return selected_tasks

def ai_move(city, world):
    selected_tasks = select_ai_move(city, world)
    for task in selected_tasks:
        city.update_task_endturn(task, world.turn)
        if task.type == "Move Troops":
            city.army -= task.data[0]
    update_building_slots(city, selected_tasks)
    city.current_tasks = selected_tasks
    cost = city.required_res(selected_tasks)
    city.spend_res(cost)

def npc_move(city, turn):
    options = possible_tasks_npc(city)
    weights = list(range(1, len(options)+1)).reverse()
    selected_tasks = choices(options, weights)[0]
    for task in selected_tasks:
        city.update_task_endturn(task, turn)
    update_building_slots(city, selected_tasks)
    city.current_tasks = selected_tasks
    city.spend_res(city.required_res(selected_tasks))

def simulate(n_turns, n_ais, nth_attempt):
    players = [Player("Tester", [])]
    players += [Player(f"AI {i}", []) for i in range(n_ais)]
    npc_count = len(players)*6
    npcs = [Player(f"NPC {i}", []) for i in range(npc_count)]
    world = World(players)
    world.players += npcs
    world.start_game()

    for _ in range(n_turns):
        world.next_turn()

    with open(f"saves/{n_turns}-{nth_attempt}", "wb") as file:
        pickle.dump(world, file)
    
for (i, j) in [(50, 7), (100, 5), (150, 4), (200, 3), (250, 3)]:
    for k in range(1, 6):
        simulate(i, j, k)