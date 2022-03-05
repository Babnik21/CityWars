from random import shuffle, sample
from math import ceil, floor
import values
import pathlib

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("saves/.") if isfile(join("saves/.", f))]

print(onlyfiles)

class Task():
    def __init__(self, type=None, data=None, end_turn=None):
        self.type = type
        self.data = data
        self.end_turn = end_turn
    
    def __eq__(self, other):
        if self.type != "Move Troops":
            return self.data[0] == other.data[0] and self.type == other.type
        else:
            return False


initial_count = 0
for path in pathlib.Path("saves/.").iterdir():
    if path.is_file():
        initial_count += 1

print(initial_count)






