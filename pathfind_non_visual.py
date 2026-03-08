import heapq
import math
import time

# imports for utility later

class Box:
    def __init__(self, position, goal, a=0, origin=None):   # arguments needed to define a Box object if not given but written below it can or has to be calculated from other arguments

        self.position = position      # index of grid (matrix) in form of (x, y)
        self.a = a                    # actual cost from start (g)
        self.b = math.sqrt((position[0]-goal[0])**2 + (position[1]-goal[1])**2)  # pythagoras from goal to self.position (heuristic) <-- (direct way)
        self.total = self.a + self.b  # total cost = a_cost + b_cost
        self.origin = origin          # parent Box, box which created this box (through surrounder)

    def __lt__(self, other):        # arguments to compare two objects are two objects
        return self.total < other.total     # adds a < and > ability to class, basically allows the class objects to be sorted in a list (by looking at total), (wasn't able to do before this because how ould you compare multiple values with one another?)

def surrounder(box, grid):  # takes a Box object and the grid (matrix), gets called for every position of a Box in visited dictionary
  
    neighbors = []  # list init
    x, y = box.position     # done for easier access of [0] and [1] of position, (also more readable)


    directions = [                    # hard coded coords(on matrix) from origin box, list of indieces (multiple of index) of neighboring Box, (directons are  basically vectors)
        (-1,0),(1,0),(0,-1),(0,1),    # orthogonal, straight away from origin box (manhattan (North, South, West, East))
        (-1,-1),(-1,1),(1,-1),(1,1)   # diagonal, diagonaly away from origin box (square root)
    ]



    for dx, dy in directions:         # easier access of directions[0] and directions[1] and loop through items in directions --> len(direction) will always be 8
        nx, ny = x + dx, y + dy       # calculate new neighbor coords through index vector + current box index
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:    # clamp so obstacles dont get overwritten by an option field, edge case for leaving grid (matrix)
            move_cost = math.sqrt(2) if dx != 0 and dy != 0 else 1      # calculate walking cost --> later important to calculate a_cost (distance from a to current position) can either be 1 or 1.4 (orthogonal or diagonal)
            neighbors.append(((nx, ny), move_cost))     # add position and move_cost (attributes of a neighbor) to the list neighbors (things needed to define a neighbour)
    return neighbors    # return the neighbors list when finished looping through directions (can be everything between 0 and 8)

def a_star(start, goal, grid):  # function that combines is the only one that is called --> it calls the other functions in itself

    open_list = []      # creates list that'll contain all option boxes which one can choose, will not be chosen randomly but rather by the total cost and if more than one the same then chosen by lowest b cost
    
    heapq.heapify(open_list)  # heapifys a list into an heap --> heap is a list that is sorted by lowest number already, way faster access
    start_box = Box(start, goal, a=0, origin=None)  # create a Box type object at the given Starting position, a is set to 0 since a coost is calculated to the start --> has to be 0, and origin to None since it has no origin, its the origin of future origins
    heapq.heappush(open_list, start_box)    # add the newly created starting box object to the heap (append for a heap)
    
    visited = {}  # stores the current box object in a dictionary (visited) and uses tuples as keys tuples which have the positions (index)on the grid on which will be box object, stores the already checked boxes (boxes on which surrounder was already called on)

    while open_list:    
        current = heapq.heappop(open_list)   # heappop deletes the smallest item of the list ad returns it at the same time, so current was the smallest object in heap before deleting
        
        if current.position == goal:       # chack if goal was reached, if position of current box is the same as position of goal 
            # reconstructs path from origin thorugh looking at origin boxes of origin boxes ...
            path = []   # path stores will store the positions of finalized quickest path from start to goal
            while current:  # loop that is going until current is False (None is recongnized as False), will loop through the origin of old boxes until current box is start where origin is set to None since its the start
                path.append(current.position)   # adds the current position of current_box to path list (position as indeieces (index plural))
                current = current.origin    # it has done all it has to do with the old box so old boxes origin is now current box, now loops until current box is start where origin is set to None so it'll break the while loop
            path.reverse()  # reverse the list because its now  built from goal to start, but start to goal is expected and more intuitive
            return path     # returns the path list with all position of path items from start to goal
        
        if current.position in visited:     # if the current position already has an entry in dictionary (visited), done to not check visited fields again and again but rather do them once
            continue    # if above statement true then continue (skips the rest of this loop and jumps to the the next iteration), so if this runs line one below wont run in this iteration
        visited[current.position] = current     # adds a new entry in the visited dict --> tuple used as key (current.position), value for this key will be the current box object

        for neighbor_pos, move_cost in surrounder(current, grid):   # iterate through the returned neighbors list, neighbor_pos is at neighbors[0] and move cost at [1], loop through list and init of both for easier access, list fromat ([(0 , 0, 0), 0])
            new_a = current.a + move_cost   # new a is calculated through sum up of cost until now + current a, sum up is basically path cost until now without current box
            if neighbor_pos not in visited or new_a < visited[neighbor_pos].a:     # if the neighbor pos is already in visited dictionary it means it was already surrounded and checked, this line ensures that this is not done twice --> wasted time or is true when new_a is the total cost to reach this neighbor from the start via the current path visited[neighbor_pos].a is the best cost we’ve previously recorded for this neighbor --> allows for quickest path
 
                neighbor_box = Box(neighbor_pos, goal, a=new_a, origin=current)     # creates a neighbor box with attributes new_a, origin is the current box since it was the one who created it (calling surrounder)
                heapq.heappush(open_list, neighbor_box)     # adds the newly created neighbor list into the heap --> then may be checked later and enhanced to be in visited dict

    # return None  # this will only run if goal is never hitted, and will return None instead of list

grid = [[0]*100]*100
start = (0,0)
goal = (99,99)
start_t = time.perf_counter_ns()
# path = a_star(start, goal, grid)
print((time.perf_counter_ns()-start_t)/1000000000)
# print(path)