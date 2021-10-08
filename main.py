import pygame as pg
import sys
import math
import random as rand
import time
from calc_util import AngledVector # Custom class for calculations

"""
[#$%] Table of Contents [%$#]
  - Const vars - some configuration options and important flags
  - Init pygame - some init for pygame, not important ¯\_(ツ)_/¯
  - Functions - used for drawing and as main logic
    |- draw_line() - draws line from one point to another
    \- koch() - main drawing logic based on recursion
  - Main - starting point of the program
"""

#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
# Const vars

DEBUG = False   # Debug mode
ITERATIONS = 5  # Number of recursions, going above 5 might take a long while
START_POS = (0.0, 4.0)
END_POS = (9.0, 4.0)

WIN_WIDTH = 1280
WIN_HEIGHT = 720
WIN_TITLE = "Koch's Curve"
WIN_PADDING = 5 # Padding from top and left window edges

COLOR_RAND = True # Bool for random colors
COLORS = {        # Some colors
  'black': (0, 0, 0),
  'white': (255, 255, 255),
  'red': (255, 0, 0),
  'green': (0, 255, 0),
  'blue': (0, 0, 255)
}

PAUSE_BETWEEN_DRAWS = True  # Bool for short pause between drawing lines
DRAW_PAUSE_LENGTH = 0.005   # Time between drawing each line in seconds
SCALE_MULTI = 120           # Drawing scale multiplier


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
# Init pygame

pg.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption(WIN_TITLE)
screen.fill(COLORS['black'])


#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
# Functions

def draw_line(x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int] = (255, 255, 255)):
  points = [
    (x1 * SCALE_MULTI + WIN_PADDING, y1 * SCALE_MULTI + WIN_PADDING),
    (x2 * SCALE_MULTI + WIN_PADDING, y2 * SCALE_MULTI + WIN_PADDING)
  ]

  # If recursion is big enough a noticable pause between drawing lines will happen anyway, exactly due to recursion (probably)
  if PAUSE_BETWEEN_DRAWS:
    time.sleep(DRAW_PAUSE_LENGTH)

  pg.draw.lines(screen, color, width = 1, closed = False, points = points)
  pg.display.update()

  if DEBUG:
    print(f"DRAW: ({x1}, {y1}) => ({x2}, {y2})")


def koch(start: tuple[float, float], end: tuple[float, float], iter: int = 3, color: tuple[int, int, int] = (255, 255, 255)):
  x1, y1 = start
  x2, y2 = end

  # Colouring
  if COLOR_RAND: 
    color = (rand.randint(1, 255), rand.randint(1, 255), rand.randint(1, 255))

  # Last call of recursion
  if iter < 1: 
    return draw_line(x1, y1, x2, y2, color)


  # 1/3rd of length from 'start' to 'end'
  third_length = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)) / 3

  # Create new custom vector class instance for this koch curve and start calculating its curve. Starting angle is calculated with calc_angle function and later angles are added to it with negative values going clockwise
  vect = AngledVector() 
  vect.move(third_length, vect.calc_angle(x1, y1, x2, y2))


  # Draws left floor
  koch((x1, y1), (x1 + vect.x, y1 - vect.y), iter = iter - 1, color = color)

  # Draws left arm
  x1 += vect.x
  y1 -= vect.y
  vect.move(third_length, 60)
  koch((x1, y1), (x1 + vect.x, y1 - vect.y), iter = iter - 1, color = color)

  # Draws right arm
  x1 += vect.x
  y1 -= vect.y
  vect.move(third_length, -120)
  koch((x1, y1), (x1 + vect.x, y1 - vect.y), iter = iter - 1, color = color)

  # Draws left floor
  x1 += vect.x
  y1 -= vect.y
  vect.move(third_length, 60)
  koch((x1, y1), (x1 + vect.x, y1 - vect.y), iter = iter - 1, color = color)




#=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
# Main

def main():
  koch(START_POS, END_POS, iter = ITERATIONS)
  pg.display.update()

  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()

if __name__ == "__main__":
  main()