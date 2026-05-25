import pygame as pg
import numpy as np
import time
import random as r



"""
(255, 255, 255)    white
(255, 0, 0)        red
(255, 255, 0)      yellow
(0, 255, 0)        green
(0, 255, 255)      cyan 
(0, 0, 255)        blue
(255, 0, 255)      purple
(0, 0, 0)          black
(46, 150, 172)     best
"""



pg.font.init()
pg.display.init()      

game_loop = True
size = 4
width, height = 400, 200  
screen = pg.display.set_mode((width*size, height*size))   
font = pg.font.Font(None, 40)
field_size = 25
started = True
end_reached = False
refined_surrounders = []
options = []

"""
Init Stuff
"""

rows = height * size // field_size
cols = width * size // field_size
sqaure_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
random_start = (0, 0)
random_end = (cols-1, rows-1)
sqaure_matrix[random_start[1]][random_start[0]] = 2
sqaure_matrix[random_end[1]][random_end[0]] = 3




class Box:

    start = random_start
    destination = random_end

    def __init__(self, box_matrix_indices: tuple, box_type: str, box_origin = None, walked_distance: int = 10):

        self.position = box_matrix_indices
        self.type = box_type
        self.box_origin = box_origin
        self.walked_distance = walked_distance



        if self.type == "start":
            self.a_cost = 0

        else:
            self.a_cost = self.calculate_a_cost()

        self.b_cost = round(np.sqrt((box_matrix_indices[0] - random_end[0])**2 + (box_matrix_indices[1] - random_end[1])**2) * 10)
        self.total_cost = self.a_cost + self.b_cost
        


    def calculate_a_cost(self):
        if self.box_origin != None:
            return self.box_origin.a_cost + self.walked_distance
        
        return -1
    

    def surrounder(self):

        origin = self
        box_matrix_indices = self.position

        raw_sorrounders = [
            (box_matrix_indices[0] - 1, box_matrix_indices[1] - 1, 14),
            (box_matrix_indices[0] - 1, box_matrix_indices[1], 10),
            (box_matrix_indices[0] - 1, box_matrix_indices[1] + 1, 14),
            (box_matrix_indices[0], box_matrix_indices[1] - 1, 10),
            (box_matrix_indices[0], box_matrix_indices[1] + 1, 10),
            (box_matrix_indices[0] + 1, box_matrix_indices[1] - 1, 14),
            (box_matrix_indices[0] + 1, box_matrix_indices[1], 10),
            (box_matrix_indices[0] + 1, box_matrix_indices[1] + 1, 14)
        ]

        refined_sorrounders = []

        for box_coord in raw_sorrounders:

            x = box_coord[0]
            y = box_coord[1]

            if x >= 0 and  y >= 0 and y < len(sqaure_matrix) and x < len(sqaure_matrix[0]):

                if sqaure_matrix[y][x] == 0 or sqaure_matrix[y][x].type == "option":
                    refined_sorrounders.append(box_coord)

                else:
                    continue


        for box_coord in refined_sorrounders:

            new_box = Box((box_coord[0], box_coord[1]), "option", box_origin=origin, walked_distance=box_coord[2])

            if sqaure_matrix[box_coord[1]][box_coord[0]] == 0 or new_box.a_cost < sqaure_matrix[box_coord[1]][box_coord[0]].a_cost:
                sqaure_matrix[box_coord[1]][box_coord[0]] = new_box
                if isinstance(sqaure_matrix[box_coord[1]][box_coord[0]], Box):
                    if new_box in options:
                        options.remove(new_box)
                    print("removed")
                options.append(new_box)




    def __lt__(self, other):
        if self.total_cost < other.total_cost:
            return True
        elif self.total_cost == other.total_cost and self.b_cost < other.b_cost:
            return True
        
        return False
    
    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        if self.position == other.position and self.type == other.type:
            return True
        return False
        
        
        














sqaure_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
random_start = (0, 0)
random_end = (cols-1, rows-1)
sqaure_matrix[random_start[1]][random_start[0]] = Box((random_start), "start")
sqaure_matrix[random_end[1]][random_end[0]] = Box((random_end), "end")







# col = 12
# start_row = 0
# end_row = 30

# for y in range(start_row, end_row + 1):
#     sqaure_matrix[y][col] = Box((col, y), "obstacle")


# col = 50
# start_row = 1
# end_row = 31

# for y in range(start_row, end_row + 1):
#     sqaure_matrix[y][col] = Box((col, y), "obstacle")

row = 15
start_col = 1
end_col = 63

for x in range(start_col, end_col + 1):
    sqaure_matrix[row][x] = Box((x, row), "obstacle")







clock = pg.time.Clock()   
counter = 0

while game_loop:   

    clock.tick()    
    mouse_pos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()  
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE] or keys[pg.K_q]:

            game_loop = False    
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and started == True:
                sqaure_matrix[random_start[1]][random_start[0]].surrounder()
                started = False

    
        # if started == True:
        #     sqaure_matrix[random_start[1]][random_start[0]].surrounder()
        #     started = False

            
    if started == False:

        start=time.perf_counter_ns()
        options.sort()
        print(time.perf_counter_ns() - start, len(options))


        choice = options[0]
        choice.type = "selected"
        choice.surrounder()
        options.pop(0)


        if choice.b_cost <= 14:
            current = choice
            while current.type != "start":
                current.type = "path"
                current = current.box_origin
                if current.a_cost <= 14:
                    end_reached = True
    
    else:
        counter = -1


                     
                        


    screen.fill((150, 150, 150))  



    for row in range(len(sqaure_matrix)):
        for col in range(len(sqaure_matrix[row])):
            coords = (col * field_size, row * field_size)
            
            x = coords[0]
            y = coords[1]

            if sqaure_matrix[row][col] == 0:
                pg.draw.rect(screen, (255, 255, 255), (x, y, field_size, field_size), 1)
                pg.draw.circle(screen, (255, 0, 0), coords, 2)

            elif sqaure_matrix[row][col].type == "obstacle":
                pg.draw.rect(screen, (0, 0, 0), (x, y, field_size, field_size))

            elif sqaure_matrix[row][col].type == "option":
                pg.draw.rect(screen, (255, 128, 0), (x, y, field_size, field_size))        
                # box_cost_string = font.render(f"a{sqaure_matrix[row][col].a_cost}, b{sqaure_matrix[row][col].b_cost}, t{sqaure_matrix[row][col].total_cost}", True, (0, 0, 0)) 
                # text_width, text_height = box_cost_string.get_size()
                # screen.blit((box_cost_string), (x + field_size//2 - text_width//2, y + field_size//2 - text_height//2))

            elif sqaure_matrix[row][col].type == "selected":
                pg.draw.rect(screen, (255, 255, 0), (x, y, field_size, field_size))
                # box_cost_string = font.render(f"a{sqaure_matrix[row][col].a_cost}, b{sqaure_matrix[row][col].b_cost}, t{sqaure_matrix[row][col].total_cost}", True, (0, 0, 0)) 
                # text_width, text_height = box_cost_string.get_size()
                # screen.blit((box_cost_string), (x + field_size//2 - text_width//2, y + field_size//2 - text_height//2))

            elif sqaure_matrix[row][col].type == "path":
                pg.draw.rect(screen, (0, 0, 255), (x, y, field_size, field_size))
                # box_cost_string = font.render(f"final", True, (0, 0, 0)) 
                # text_width, text_height = box_cost_string.get_size()
                # screen.blit((box_cost_string), (x + field_size//2 - text_width//2, y + field_size//2 - text_height//2))








    for event in events: 
        if event.type == pg.MOUSEBUTTONDOWN:
                
            x = mouse_pos[0] // field_size
            y = mouse_pos[1] // field_size

            if event.button == 2:

                if sqaure_matrix[y][x] == 0:

                    sqaure_matrix[y][x] = Box((x, y), "obstacle")

                if sqaure_matrix[y][x].type == "option": 

                    box = sqaure_matrix[y][x]
                    sqaure_matrix[y][x] = Box((x, y), "obstacle")
                    # options.append(box)

                    
            # if event.button == 1:
            #     if type(sqaure_matrix[y][x]) == Box:
            #         if sqaure_matrix[y][x].type == "option":
            #             box = sqaure_matrix[y][x]
            #             box.type = "selected"
            #             box.surrounder()

            # if event.button == 3:
            #     if type(sqaure_matrix[y][x]) == Box:
            #         if sqaure_matrix[y][x].type == "obstacle":
            #             sqaure_matrix[y][x] = 0
                    








    pg.draw.rect(screen, (255, 0, 255), (random_start[0] * field_size, random_start[1] * field_size, field_size, field_size), 3)
    pg.draw.rect(screen, (0, 255, 0), (random_end[0] * field_size, random_end[1] * field_size, field_size, field_size), 3)
    # print(selected_boxes)
    # screen.blit((box_cost_string), (3 * field_size + field_size//2 - text_width//2, 3 * field_size + field_size//2 - text_height//2)) #(Box.position[0] * field_size + field_size//2, Box.position[1] * field_size + field_size//2)
    # print(f"end{refined_surrounders}")
    counter += 1
    counter_string = font.render(f"c_value: {counter}", True, (0, 0, 0)) 
    # print(counter)
    screen.blit((counter_string), (width//2 * size, 0)) 

    pg.display.update()   



    if end_reached:
        time.sleep(1)
        game_loop = False

      

pg.quit()

# for option in options:
#     print(f"{option.position}")

counter_o = 0

for row in range(len(sqaure_matrix)):
    for col in range(len(sqaure_matrix[row])):
        if isinstance(sqaure_matrix[row][col], Box) and sqaure_matrix[row][col].type == "option":
            counter_o += 1

print(counter_o)