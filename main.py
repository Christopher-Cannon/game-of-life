import pygame
import random
from enum import Enum
import os.path
from os import path

def nextGeneration(grid):
  # Create a blank grid to write to
  next_gen = [[0 for x in range(int(WIDTH/10))] for y in range(int(HEIGHT/10))]
  # Neighbour cell coordinates
  neighbours = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
  cur_row = 0
  # Iterate through the grid
  for row in grid:
    for col in range(len(row)):
      # Determine how many neighbours this cell has
      neighbour_count = 0

      for co in neighbours:
        try:
          if grid[cur_row + co[1]][col + co[0]] == 1:
            neighbour_count += 1
        except:
          continue

      # Determine what to do if this cell is live or dead
      if grid[cur_row][col] == Status.LIVE:
        # Die due to under/overpopulation
        if neighbour_count > 1 and neighbour_count < 4:
          next_gen[cur_row][col] = Status.LIVE
        else:
          next_gen[cur_row][col] = Status.DEAD
      else:
        # Come to life if 3 neighbours
        if neighbour_count == 3:
          next_gen[cur_row][col] = Status.LIVE

    cur_row += 1

  return next_gen

def randomGeneration():
  random_grid = [[0 for x in range(int(WIDTH/10))] for y in range(int(HEIGHT/10))]

  cur_row = 0

  for row in random_grid:
    for col in range(len(row)):
      if random.randint(0, 10) > 4:
        random_grid[cur_row][col] = 1

    cur_row += 1

  return random_grid

current_path = os.path.dirname(__file__)
resource_path = os.path.join(current_path, 'resources')

pygame.init()
clock = pygame.time.Clock()

WIDTH = 500
HEIGHT = 500
WAIT_TIME = 125

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life")

class Status:
  DEAD = 0
  LIVE = 1

current_gen = [[0 for x in range(int(WIDTH/10))] for y in range(int(HEIGHT/10))]

LIVE_CELL = pygame.image.load(os.path.join(resource_path, 'live.png'))
DEAD_CELL = pygame.image.load(os.path.join(resource_path, 'dead.png'))

running = True
start = False

while running:
  screen.fill((0, 0, 0))

  cell_x = 0
  cell_y = 0
  # Output grid of cells
  for row in current_gen:
    for col in row:
      if col == Status.LIVE:
        screen.blit(LIVE_CELL, (cell_x*10, cell_y*10))
      else:
        screen.blit(DEAD_CELL, (cell_x*10, cell_y*10))

      cell_x += 1
    cell_x = 0
    cell_y += 1

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(start):
      mouse_x, mouse_y = event.pos

      while mouse_x % 10 != 0:
        mouse_x -= 1

      while mouse_y % 10 != 0:
        mouse_y -= 1

      if current_gen[int(mouse_y/10)][int(mouse_x/10)] == Status.LIVE:
        current_gen[int(mouse_y/10)][int(mouse_x/10)] = Status.DEAD
      else:
        current_gen[int(mouse_y/10)][int(mouse_x/10)] = Status.LIVE

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        start = not(start)

      if event.key == pygame.K_r:
        current_gen = randomGeneration()

      if event.key == pygame.K_c:
        current_gen = [[0 for x in range(int(WIDTH/10))] for y in range(int(HEIGHT/10))]

  if start:
    current_gen = nextGeneration(current_gen)

  pygame.display.update()
  clock.tick(60)
  pygame.time.wait(WAIT_TIME)
