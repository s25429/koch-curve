from dataclasses import dataclass, field
from math import sin, cos, pi as PI

@dataclass
class AngledVector:
  """This class is used as a storing place for currently being claculated part of koch's curve and as a place for calculating all the angles"""

  angle: float = 0
  x: float = field(init = False, default = 0)
  y: float = field(init = False, default = 0)


  def get_line_dir(self, a: float, b: float) -> int:
    """
    Returns an int that specifies which direction the line is leaning to.
    For x params: 0 - horizontal line,  1 - goes right, -1 - goes left
    For y params: 0 - vertical line,    1 - goes down,  -1 goes up
    """

    # Points positions have to be checked first for a straight line with rounding function, as the floating point might be slightly off from calculations on a very small scale. Irregularities only matter in checking if two points are equal.
    if round(a, 6) == round(b, 6):  return 0
    elif a < b:                     return 1
    else:                           return -1


  def calc_angle(self, x1, y1, x2, y2) -> int:
    """Calculates the angle in degrees of inclination to the X axis"""

    dir_x = self.get_line_dir(x1, x2)
    dir_y = self.get_line_dir(y1, y2)

    if dir_y == 0:                # y1 == y2
      if dir_x > 0:   return 0    #   x1 < x2   (1, 0)
      elif dir_x < 0: return 180  #   x1 > x2   (-1, 0)
      else:           return None #   x1 == x2  (0, 0)  <- impossible to reach
    elif dir_y > 0:               # y1 < y2
      if dir_x > 0:   return 300  #   x1 < x2   (1, 1)
      elif dir_x < 0: return 240  #   x1 > x2   (-1, 1)
      else:           return 270  #   x1 == x2  (0, 1)
    elif dir_y < 0:               # y1 > y2
      if dir_x > 0:   return 60   #   x1 < x2   (1, -1)
      elif dir_x < 0: return 120  #   x1 > x2   (-1, 1)
      else:           return 90   #   x1 == x2  (0, -1)
    else: 
      return None 
      # None, because there is literally nothing to be done for some reason. This should never get to it here though


  def move(self, d: float, angle: float):
    """Calculates position based of line length (d) and angle of inclination to the X axis (angle)"""

    self.x = d * cos((self.angle + angle) * PI / 180)
    self.y = d * sin((self.angle + angle) * PI / 180)
    self.angle += angle
