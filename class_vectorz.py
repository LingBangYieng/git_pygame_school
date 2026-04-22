import numpy as np


class Vectorz:


    def __init__(self, x, y):
        
        self.tuple = (x, y)
        self.x = x
        self.y = y

    @property
    def magnitude(self):
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def direction(self):
        return Vectorz(self.x / self.magnitude, self.y / self.magnitude)
        

    def __add__(self, other):
        if isinstance(other, Vectorz):
            return Vectorz(self.x + other.x, self.y + other.y)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vectorz):
            return Vectorz(self.x - other.x, self.y - other.y)
        else:
            raise TypeError
        
    def __mul__(self, other):
        if isinstance(other, Vectorz):
            return ((self.x * other.x) + (self.y * other.y))
        
        elif isinstance(other, (int, float)):
            return Vectorz(self.x * other, self.y * other)
        else:
            raise TypeError
    
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vectorz(self.x / other, self.y / other)
        else:
            raise TypeError
        
    def __repr__(self):
        return f"V({self.x}, {self.y})"