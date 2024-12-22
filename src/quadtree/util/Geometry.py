from __future__ import annotations
from typing import Self

class Point:
  """
  Dummy class for points, can be used later, for now it finds no application
  """
  def __init__(self,x: float,y: float):
    self.x = x
    self.y = y 

  def __str__(self: Self) -> str:
    return f"({self.x},{self.y})"

  def __eq__(self: Self, other: Self) -> bool:
    return self.x == other.x and self.y == other.y
    
  def __lt__(self: Self, other: Self) -> bool:
    return self.x < other.x and self.y < other.y

  def __gt__(self: Self, other: Self) -> bool:
    return self.x > other.x and self.y > other.y
    
  def __le__(self: Self, other: Self) -> bool:
    return self.x <= other.x and self.y <= other.y
    
  def __ge__(self: Self, other: Self) -> bool:
    return self.x >= other.x and self.y >= other.y
    
  def __iter__(self: Self) -> tuple[float,float]:
    return (self.x,self.y)
    
  def __getitem__(self: Self,index: int) -> float:
    match index:
      case 0:
        return self.y
      case 1:
        return self.y
      case _:
        raise ValueError("There is not such dimension")
              
class Area:
  def __init__(self,bottom_left: Point, upper_right: Point):
    self.bottom_left = bottom_left
    self.upper_right = upper_right 
      
  def __str__(self: Self) -> str:
    return f"[{self.bottom_left}:{self.upper_right}]"
  
  def contains_area(self: Self, area: Area):
    return area.upper_right <= self.upper_right and area.bottom_left >= self.bottom_left
  
  def intersects_with_area(self: Self, area: Area):
    return (
      area.upper_right.x > self.bottom_left.x and 
      area.bottom_left.x < self.upper_right.x and
      area.upper_right.y > self.bottom_left.y and
      area.bottom_left.y < self.upper_right.y
    )
  
  def contains_point(self: Self, point: Point):
    return (
      self.bottom_left.x <= point.x <= self.upper_right.x and
      self.bottom_left.y <= point.y <= self.upper_right.y
    )
    