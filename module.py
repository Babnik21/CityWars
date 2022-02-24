from random import choice
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
        

class City():
    def __init__(self, owner, size, coords =(0,0)):
        self.owner = owner
        self.size = size
        self.coords = coords
        self.buildings = {}
        for i in range(size+1):
            self.buildings[i] = Building()
        self.army = Army()
        # Change default resource values
        self.resources = (10, 10, 10)

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
world1.map[c].build("Bank", 3)
print(world1.map[c])
world1.map[c].upgrade("Bank")
print(world1.map[c])
world1.map[c].train("Unit2", 10)
world1.map[c].train("Spy", 1)
print(world1)
print(world1.map[c])
'''

