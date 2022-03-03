from random import shuffle, sample
from math import ceil, floor
import values

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

for i in range(4):
    print(i//2, i%2)



