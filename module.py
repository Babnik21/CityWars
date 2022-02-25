from random import choice

farm_prod = 50
iron_prod = 10
gold_prod = 2

class World():
    def __init__(self, players):
        self.size = 2 + len(players)
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

    #Adds a new city on the map (returns coords for now)
    def spawn_city(self, owner, size):
        coords = choice(self.empty_coords)
        city = City(owner, size, coords)
        self.cities.append(city)
        self.empty_coords.remove(coords)
        self.map[coords] = city
        return coords

    def next_turn(self):
        for city in self.cities:
            city.update_res()
            for task in city.current_tasks:
                if task.type != None:
                    city.ongoing_tasks.append(task)
            city.current_tasks = []
            self.turn += 1
            delete = []
            for task in city.ongoing_tasks:
                if task.end_turn == self.turn:
                    city.execute(task)
                    delete.append(task)
            city.ongoing_tasks = [item for item in city.ongoing_tasks if item not in delete]
            

        

class City():
    def __init__(self, owner, size, coords=(0,0)):
        self.owner = owner
        self.size = size
        self.coords = coords
        self.buildings = {}
        for i in range(size+1):
            self.buildings[i] = Building()
        self.army = Army()
        # Change default resource values
        self.resources = [10, 10, 10]
        self.current_tasks = []
        self.ongoing_tasks = []

    def buildings_to_str(self):
        string = ""
        for key in self.buildings.keys():
            string += str(self.buildings[key])
        return string

    def __repr__(self):
        return f"City owned by {self.owner} at {self.coords}. \nArmy: \n" + str(self.army) + "\nBuildings: \n" + self.buildings_to_str()

    def train(self, units, num):
        # Dodaj še: Check if enough available resources and training camp is built, deduct resources:
        if True:
            self.army.train(units, num)

    def check_build(self, b, slot):
        # Checks if building slot is empty - Dodaj še da preveri surovine
        if self.buildings[slot] == Building():
            return True, None
        else:
            return False, "Can't build"

    def build(self, b, slot):
        # Dodaj da odšteje surovine
        self.buildings[slot] = Building(b, 1)
    
    def check_upgrade(self, slot):
        # Checks if a building exists on selected slot - Dodaj še da preveri surovine
        if self.buildings[slot].level not in [0,5]:
            return False, "Nothing is built there"
        else:
            return True, None

    def exists(self, building):
        for b in self.buildings:
            if self.buildings[b].type == building:
                return True
        return False

    def find_slot(self, building):
        for s in self.buildings:
            if self.buildings[s].type == building:
                return s
        return "Error"

    def upgrade(self, b):
        # Dodaj da odšteje surovine
        slot = self.find_slot(b)
        type = self.buildings[slot].type
        lvl = self.buildings[slot].level
        self.buildings[slot] = Building(type, lvl+1)

    def execute(self, task):
        if task.type == "Build":
            self.build(task.data[0], task.data[1])
            print(f"Building {task.data[0]}")
        elif task.type == "Upgrade":
            self.upgrade(task.data[0])
            print(f"Upgrading {task.data[0]}")
        elif task.type == "Attack":
            print("Attacking yadi yada")     #Execute build -- dodaj to
        elif task.type == "Return":
            print("Returning yadi yada")     #Execute -- dodaj to 
        elif task.type == "Train":
            self.army.units[task.data[0]] += task.data[1]
            print(f"Training {task.data[1]} of {task.data[0]}")

    def update_res(self):
        gold = 0
        iron = 0
        food = 10
        for s in self.buildings:
            if self.buildings[s].type == "Farm":
                food += self.buildings[s].level*farm_prod
            elif self.buildings[s].type == "Iron Mine":
                iron += self.buildings[s].level*iron_prod
            elif self.buildings[s].type == "Gold Mine":
                gold += self.buildings[s].level*gold_prod
        self.resources = [self.resources[0] + food, self.resources[1] + iron, self.resources[2] + gold]
        
class Task():
    def __init__(self, type=None, data=None, end_turn=None):
        self.type = type
        self.data = data
        self.end_turn = end_turn

    def __str__(self):
        return f"Task of type {self.type}. Completed on turn {self.end_turn}."

    def __repr__(self):
        return f"Task({self.type}, {self.data}, {self.end_turn})"

class Report():
    def __init__(self, a_vil, d_vil, turn, type):
        self.turn = turn
        self.a_vil = a_vil
        self.d_vil = d_vil
        self.type = type
        
    def __repr__(self):
        if self.type == "Attack":
            return "Attack blabla"
        elif self.type == "Raid":
            return "Raid blabla"
        elif self.type == "Conquest":
            return "Conquest blabla"
        

class Army():
    def __init__(self):
        self.units = {
            "Unit1": 0,
            "Unit2": 0,
            "Unit3": 0,
            "Spy": 0,
            "Conqueror": 0
        }

    def train(self, unit, num):
        self.units[unit] += num

    def __repr__(self):
        return f"Unit1: {self.units['Unit1']},\nUnit2: {self.units['Unit2']},\nUnit3: {self.units['Unit3']},\nSpy: {self.units['Spy']},\nConqueror: {self.units['Conqueror']}\n"

    def __str__(self):
        return f"Unit1: {self.units['Unit1']},\nUnit2: {self.units['Unit2']},\nUnit3: {self.units['Unit3']},\nSpy: {self.units['Spy']},\nConqueror: {self.units['Conqueror']}\n"
        
class Building():
    def __init__(self, type="Empty", level=0):
        self.type = type
        self.level = level
        self.img = "Dodaj path do slike glede na type"    ##

    def __str__(self):
        return f"{self.type} (lvl {self.level})\n"

'''
world1 = World(["Babnik"])
c = world1.spawn_city("Babnik", 6)
print(world1.map[c])
world1.map[c].current_tasks.append(Task("Build", ["Bank", 1], 7))
world1.map[c].current_tasks.append(Task("Upgrade", ["Bank"], 7))
world1.map[c].current_tasks.append(Task("Train", ["Unit2", 5], 5))
world1.map[c].current_tasks.append(Task("Build", ["Iron Mine", 5], 4))
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
world1.next_turn()
print(world1.map[c].ongoing_tasks)
print(world1.map[c].resources)
print(world1)
print(world1.map[c])
'''

