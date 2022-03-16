from random import shuffle, sample, uniform, choice, choices
from math import ceil, floor
import values
import pathlib
import pickle
import os
import re


class Task():
    def __init__(self, type=None, data=None, end_turn=None):
        self.type = type
        self.data = data
        self.end_turn = end_turn
    
    def __eq__(self, other):
        if isinstance(other, Task):
            if self.type == "Build" and other.type == "Build":
                return self.data[0]==other.data[0] or self.data[1] == other.data[1]
            elif self.type in ["Upgrade", "Train"]:
                return self.data[0] == other.data[0] and self.type == other.type
        return False



class Test():
    def __init__(self):
        self.type = "Alpha"
        self.second = f"Jaz sem {self.type}"





