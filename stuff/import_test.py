import time
from pathfind_non_visual import a_star

grid = [[0]*100]*100
start = (0,0)
goal = (99,99)
start_t = time.perf_counter_ns()
path = a_star(start, goal, grid)
print((time.perf_counter_ns()-start_t)/1000000000)
print(path)
