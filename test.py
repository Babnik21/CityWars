from random import shuffle, sample
from math import ceil, floor
import values

class Aa():
    def __init__(self, lst):
        self.lst = lst

y = (1, 2, 3, 4)

z = tuple([n if n < 3 else n+10 for n in y])
print(z)

