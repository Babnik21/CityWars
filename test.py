from random import shuffle, sample

class Drek():
    def __init__(self, lst):
        self.lst = lst

a = Drek([1, 2, 3, 4, 5])
shuffle(a.lst)
print(a.lst)