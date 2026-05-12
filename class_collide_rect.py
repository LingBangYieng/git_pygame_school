class HitBox:

    def __init__(self, x, y, w, h):
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_collision(self, other)->bool:

        if (self.x < other.x) and (other.x < self.x + self.w) and (self.y < other.y) and (other.y < self.y + self.h):
            return True
        else:
            return False
