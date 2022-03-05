from random import choice, shuffle, uniform
from math import floor, ceil, sqrt
import values

class World():
    def __init__(self, players):
        self.players = players
        self.size = 2 + len(self.players)
        self.cities = []
        self.turn = 1
        lst = []
        for i in range(-self.size, self.size+1):
            for j in range(-self.size, self.size+1):
                lst.append((i,j))
        self.empty_coords = lst
        self.map = {}
        for key in self.empty_coords:
            self.map[key] = "Empty"

    def __repr__(self):
        return f"World of size {self.size*2+1}x{self.size*2+1} with {len(self.cities)} cities. Current turn: {self.turn}"

    def start_game(self):
        for p in self.players:
            self.spawn_city(p, 9)

    #Adds a new city on the map (returns coords for now)
    def spawn_city(self, player, size):
        coords = choice(self.empty_coords)
        city = City(player, size, coords, [])
        player.add(city)
        self.cities.append(city)
        self.empty_coords.remove(coords)
        self.map[coords] = city
        return coords

    def next_turn(self):
        shuffle(self.cities)
        for city in self.cities:
            for task in city.current_tasks:
                if task.type != None:                               # Is this neccessary?
                    city.ongoing_tasks.append(task)
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

class Player():
    def __init__(self, username, cities=[]):
        self.username = username
        self.cities = cities

    def __str__(self):
        return self.username
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        else:
            return False

    def add(self, city):
        #self.cities = self.cities + [city]
        self.cities.append(city)

class City():
    def __init__(self, owner, size, coords, reports):
        self.owner = owner
        self.size = size
        self.coords = coords
        self.buildings = {}
        for i in range(size+1):
            self.buildings[i] = Building(slot=i)
        self.army = Army()
        # Change default resource values
        self.resources = [150, 150, 5]
        self.current_tasks = []
        self.ongoing_tasks = []
        self.reports = reports

    def buildings_to_str(self):
        string = ""
        for key in self.buildings.keys():
            string += str(self.buildings[key])
        return string

    def __repr__(self):
        return f"City owned by {self.owner} at {self.coords}. \nArmy: \n" + str(self.army) + "\nBuildings: \n" + self.buildings_to_str()

    def __str__(self):
        return f"City owned by {self.owner.username} at {self.coords}. Current tasks: {len(self.current_tasks)}"

    def train(self, units, num):
        self.army.train(units, num)

    def build(self, b, slot):
        self.buildings[slot] = Building(b, 1, slot)

    def find_slot(self, building):
        for s in self.buildings:
            if self.buildings[s].type == building:
                return s
        return "Error"

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
                loot = [0, 0, 0]
                if task.data[3] == "Raid":                  # only executes when raiding; other attacks dont yield any loot
                    cap = r_army.capacity()                 # Calculate carrying capacity
                    loot = task.data[2].steal_res(cap)      # Remove loot from defending city
                elif task.data[3] == "Conquest" and result[4]:
                    loser = task.data[2].owner              # If conquered, change village owner
                    loser.cities.remove(task.data[2])
                    task.data[2].owner = self.owner
                    self.owner.cities.append(task.data[2])

                # Make new task for troop return
                if r_army != 0:
                    self.ongoing_tasks.append(Task("Move Troops", [r_army, task.data[2], self, "Return", loot], 2))   # Change end turn !!!!
                    self.update_task_endturn(self.ongoing_tasks[-1], curr_turn + 1)
        elif task.type == "Train":
            self.army.units[task.data[0]] += task.data[1]

    # Produces resources
    def update_res(self):
        gold, iron, food = 0,0,0
        # Add values
        food += values.farm_prod[self.find_level("Farm")] + values.bakery_prod[self.find_level("Bakery")]
        iron += values.iron_prod[self.find_level("Iron Mine")]
        gold += values.gold_prod[self.find_level("Gold Mine")]
        # Avoid overflow
        food = min(food, values.warehouse_capacity[self.find_level("Warehouse")] - self.resources[0])
        iron = min(iron, values.warehouse_capacity[self.find_level("Warehouse")] - self.resources[1])
        gold = min(gold, values.warehouse_capacity[self.find_level("Bank")] - self.resources[2])
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
        if self.resources[0] + self.resources[1] + self.resources[2] <= cap:
            loot = [self.resources[0], self.resources[1], self.resources[2]]
            self.resources = [0, 0, 0]
            return loot
        else:
            ratio_f = self.resources[0]/(self.resources[0]+self.resources[1]+self.resources[2])
            ratio_i = self.resources[1]/(self.resources[0]+self.resources[1]+self.resources[2])
            ratio_g = self.resources[2]/(self.resources[0]+self.resources[1]+self.resources[2])
            farm = floor(cap*ratio_f)
            iron = floor(cap*ratio_i)
            gold = floor(cap*ratio_g)
            self.resources = [self.resources[0] - farm, self.resources[1] - iron, self.resources[2 - gold]]
            return [farm, iron, gold]

    # Returns amount of resources required to start selected task
    def required_res(self, task):
        if task.type == "Build" or task.type == "Upgrade":
            lvl = self.find_level(task.data[0])
            return values.building_costs[task.data[0]][lvl]
        elif task.type == "Train":
            return [task.data[1] * x for x in values.unit_costs[task.data[0]]]
        else: 
            return [0,0,0]

    # Main function for checking if task is available: returns (False, error) if not and (True, required resources) if yes          Neccessary??
    def task_available(self, task):
        if task.type == "Build":
            if task.data[0] == "Wall":
                if task.data[1] != 0:
                    return False, "Can't build wall there!"
            if self.buildings[task.data[1]].type != "Empty":
                return False, "This building slot is already full!"
            elif self.find_level(task.data[0]) != 0:
                return False, "This building already exists!"
        elif task.type == "Upgrade":
            if self.find_level(task.data[0]) == 0:
                return False, "Building doesn't exist"
            elif self.find_level(task.data[0]) == 5:
                return False, "Building is already at max level!"
        # Doesn't check if destination village exists!
        elif task.type == "Move Troops":
            if task.data[0] not in self.army:
                return False, "You don't have enough troops!"
        elif task.type == "Train":
            if self.army.count() + task.data[1] > values.housing_capacity[self.find_level("Housing")]:
                return False, "You don't have enough housing capacity!"
        req = self.required_res(task)
        if self.resources[0] >= req[0] and self.resources[1] >= req[1] and self.resources[2] >= req[2]:
            return True, req
        else:
            return False, "You don't have enough resources"

    # Main function for calculating combat results --> returns (a_dead, d_dead, luck, bool_spotted, bool_conquered)
    def combat_calculation(self, task):
        luck = uniform(-0.1, 0.1)
        wall = task.data[2].find_level("Wall")
        conq = False
        a_pow = task.data[0].power("A", luck, wall)
        d_pow = task.data[2].army.power("D", luck, wall)
        if task.data[3] == "Raid" or task.data[3] == "Espionage":
            if task.data[3] == "Espionage" and task.data[2].army.units["Spy"] < 0:
                return Army([0,0,0,0,0]), Army([0,0,0,0,0]), luck, False, conq
            else:
                rate = a_pow/(a_pow + d_pow)
                d_dead = task.data[2].army * rate
                a_dead = task.data[0] * (1-rate)
                return a_dead, d_dead, luck, True, conq
        if task.data[3] == "Attack" or task.data[3] == "Conquest":
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
            return a_dead, d_dead, luck, True, conq

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
        r_atk = Report(a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, conq)
        r_def = Report(a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, conq)
        self.reports.append(r_atk)
        if spotted:
            d_city.reports.append(r_def)

    # Updates task endturn                                                                                                      TUKI SMMM¨!!!!!!!!!1
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
                return f"Troops returning from {self.data[1].coords} \nReturning army: {self.data[0]}.\nCompleted on turn {self.end_turn}"
            else: 
                return f"{self.data[3]}: {self.data[2].coords}\nArmy: {self.data[0]}\nCompleted: turn {self.end_turn}"
        else:
            return f"{self.type} {self.data[0]}. \nCompleted: turn {self.end_turn}"

    def __repr__(self):
        if self.type == "Move Troops":
            return f"Task({self.type}, Some data, type {self.data[3]}, {self.end_turn})"
        else:
            return f"Task({self.type}, Some data, {self.end_turn})"

    def __eq__(self, other):
        if isinstance(other, Task):
            if self.type == "Build" and other.type == "Build":
                return self.data[0]==other.data[0] or self.data[1] == other.data[1]
            elif self.type in ["Upgrade", "Train"]:
                return self.data[0] == other.data[0] and self.type == other.type and self.end_turn == other.end_turn
        return False

    def __lt__(self, other):
        return self.end_turn < other.end_turn

class Report():
    def __init__(self, a_city, d_city, turn, type, a_army, d_army, a_dead, d_dead, luck, read = False):
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
        
    def __repr__(self):
        return f"{self.type} on {self.d_city.coords}, turn {self.turn}."

    def __str__(self):
        headline = f"{self.type} on {self.d_city.coords}, turn {self.turn}."
        if not self.read:
            headline = "UNREAD -- " + headline
        a_army = f"Attacking army: \nInfantryman: {self.a_army.units['Infantryman']}\nSniper: {self.a_army.units['Sniper']}\nTank: {self.a_army.units['Tank']}\nSpy: {self.a_army.units['Spy']}\nGeneral: {self.a_army.units['General']}."
        a_dead = f"Casualties: \nInfantryman: {self.a_dead.units['Infantryman']}\nSniper: {self.a_dead.units['Sniper']}\nTank: {self.a_dead.units['Tank']}\nSpy: {self.a_dead.units['Spy']}\nGeneral: {self.a_dead.units['General']}."
        d_army = f"Defending army: \nInfantryman: {self.d_army.units['Infantryman']}\nSniper: {self.d_army.units['Sniper']}\nTank: {self.d_army.units['Tank']}\nSpy: {self.d_army.units['Spy']}\nGeneral: {self.d_army.units['General']}."
        d_dead = f"Casualties: \nInfantryman: {self.d_dead.units['Infantryman']}\nSniper: {self.d_dead.units['Sniper']}\nTank: {self.d_dead.units['Tank']}\nSpy: {self.d_dead.units['Spy']}\nGeneral: {self.d_dead.units['General']}."
        if self.luck > 0:
            luck = f"Attackers were lucky ({round(self.luck*100, 2)}% bonus power)"
        else:
            luck = f"Attackers were unlucky ({round(-self.luck*100, 2)}% power deduction)"
        return headline + a_army + a_dead + d_army + d_dead + luck

    def __lt__(self, other):
        return self.turn > other.turn

class Army():
    def __init__(self, units = [3,0,0,0,0]):
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
        general = ceil(self.units["General"] * other)
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
        self.img = "Dodaj path do slike glede na type"    ##

    def __str__(self):
        return f"{self.type} (lvl {self.level})\n"

def distance(c1, c2):
    return sqrt((c1.coords[0] - c2.coords[0])**2 + (c1.coords[1] - c2.coords[1])**2)


'''
world1 = World(["Babnik", "NPC"])
ca = world1.spawn_city("Babnik", 12)
cd = world1.spawn_city("NPC", 12)
world1.map[ca].reports.append(Report(world1.map[ca], world1.map[cd], 2, "Attack", Army(), Army(), Army(), Army(), 0.05))
world1.map[ca].build("Warehouse", 1)
world1.map[ca].upgrade("Warehouse")
world1.map[ca].build("Bank", 3)
world1.map[ca].upgrade("Bank")
world1.map[ca].build("Training Camp", 2)
world1.map[ca].resources = [300,300,20]
print(world1.map[ca].reports)
'''

''' Task test
t1 = Task("Train", ["Infantryman", 3], 9)
t2 = Task("Build", ["Farm", 2], 3)
t3 = Task("Move Troops", [Army([5, 0, 0, 0, 0]), world1.map[ca], world1.map[cd], "Raid"], 6)
t4 = Task("Build", ["Farm", 3], 5)
t5 = Task("Build", ["Iron Mine", 4], 7)
t7 = Task("Upgrade", ["Farm"], 7)
print(f"Can start task 1: {world1.map[ca].task_available(t1)}")
print(f"Can start task 2: {world1.map[ca].task_available(t2)}")
print(f"Can start task 3: {world1.map[ca].task_available(t3)}")
print(f"Can start task 4: {world1.map[ca].task_available(t4)}")
print(f"Can start task 5: {world1.map[ca].task_available(t5)}")
print(f"Can start task 7: {world1.map[ca].task_available(t7)}")
world1.next_turn()
print(f"Turn: {world1.turn}")
world1.map[ca].current_tasks.append(t2)
world1.next_turn()
print(f"Turn: {world1.turn}")
print(world1.map[ca].resources)
print(f"Can start task 1: {world1.map[ca].task_available(t1)}")
print(f"Can start task 2: {world1.map[ca].task_available(t2)}")
print(f"Can start task 3: {world1.map[ca].task_available(t3)}")
print(f"Can start task 4: {world1.map[ca].task_available(t4)}")
print(f"Can start task 5: {world1.map[ca].task_available(t5)}")
print(f"Can start task 7: {world1.map[ca].task_available(t7)}")
world1.next_turn()
print(f"Turn: {world1.turn}")
world1.next_turn()
print(f"Turn: {world1.turn}")
print(f"Can start task 1: {world1.map[ca].task_available(t1)}")
print(f"Can start task 2: {world1.map[ca].task_available(t2)}")
print(f"Can start task 3: {world1.map[ca].task_available(t3)}")
print(f"Can start task 4: {world1.map[ca].task_available(t4)}")
print(f"Can start task 5: {world1.map[ca].task_available(t5)}")
print(f"Can start task 7: {world1.map[ca].task_available(t7)}")
world1.map[ca].current_tasks.append(t5)
world1.next_turn()
print(f"Turn: {world1.turn}")
world1.next_turn()
print(f"Turn: {world1.turn}")
print(world1.map[ca].resources)
print(f"Can start task 1: {world1.map[ca].task_available(t1)}")
print(f"Can start task 2: {world1.map[ca].task_available(t2)}")
print(f"Can start task 3: {world1.map[ca].task_available(t3)}")
print(f"Can start task 4: {world1.map[ca].task_available(t4)}")
print(f"Can start task 5: {world1.map[ca].task_available(t5)}")
print(f"Can start task 7: {world1.map[ca].task_available(t7)}")
world1.next_turn()
print(f"Turn: {world1.turn}")
world1.map[ca].current_tasks.append(t1)
world1.next_turn()
print(f"Turn: {world1.turn}")
print(world1.map[ca].resources)
print(f"Can start task 1: {world1.map[ca].task_available(t1)}")
print(f"Can start task 2: {world1.map[ca].task_available(t2)}")
print(f"Can start task 3: {world1.map[ca].task_available(t3)}")
print(f"Can start task 4: {world1.map[ca].task_available(t4)}")
print(f"Can start task 5: {world1.map[ca].task_available(t5)}")
print(f"Can start task 7: {world1.map[ca].task_available(t7)}")
'''


#PREVERI ČE EXECUTE TASK, MAKE REPORTS IN COMBAT CALCULATION DELUJETO PRAVILNO
