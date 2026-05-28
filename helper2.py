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


def getHitBox_HBLayer():
    HBLayer = bitmap()

    MapHitBoxList = []

    for row in range(len(HBLayer)):
        for col in range(len(HBLayer[0])):
            if HBLayer[row][col]:
                MapHitBoxList.append(HitBox(tuple(e*CellSize for e in (row, col)), (CellSize, CellSize)))
                #may fiddle arround with placement of (row, col)
    
