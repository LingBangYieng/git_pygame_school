import json
def bitmap():
    grid = None
    with open("saves/test.map", "r") as f:
        grid = eval(f.read())
    layer = grid[1]
    HB_layer = [[int(isinstance(col, tuple)) for col in row] for row in layer] #iterates over and replaces with 0/1 depoending on field
    return HB_layer

def upscale_grid(grid, factor=2):
    new_grid = []

    for row in grid:
        # duplicate each value horizontally
        expanded_row = []
        for cell in row:
            expanded_row.extend([cell] * factor)

        # duplicate row vertically
        for _ in range(factor):
            new_grid.append(expanded_row.copy())

    return new_grid