# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 10:20:55 2020

@author: celine.gross
"""

with open('input_day17.txt', 'r') as file:
    puzzle = [[l for l in line.strip()] for line in file]


# Part 1

def create_positions(data):
    active = set()
    for x, row in enumerate(data):
        for y, col in enumerate(row):
            if col == '#':
                active.add((x, y, 0))
    return active


def count_neighbours(position, active):
    x, y, z = position
    count = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            for k in [z-1, z, z+1]:
                if (i, j, k) in active and (i, j, k) != position:
                    count+=1
    return count
 
    
def generate_cubes(active):
    cubes = set()
    min_x, max_x = min(active, key = lambda t: t[0])[0], max(active, key = lambda t: t[0])[0]
    min_y, max_y = min(active, key = lambda t: t[1])[1], max(active, key = lambda t: t[1])[1]
    min_z, max_z = min(active, key = lambda t: t[2])[2], max(active, key = lambda t: t[2])[2]
    
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                cubes.add((x, y, z))
    return cubes
    

def update_state(active):
    new_active = active.copy()  
    for position in generate_cubes(active):
        # Active cubes
        if position in active:
            if count_neighbours(position, active) <2 or count_neighbours(position, active)>3:
                new_active.remove(position)
        # Inactive cubes
        else:
            if count_neighbours(position, active) == 3:
                new_active.add(position)
    return new_active


def run(data, n):
    active_cubes = create_positions(data)
    for i in range(n):
        active_cubes = update_state(active_cubes)
    return len(active_cubes)
    

print(run(puzzle, 6))