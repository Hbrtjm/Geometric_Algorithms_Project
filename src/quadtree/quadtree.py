from __future__ import annotations
from util.Geometry import Area, Point
from typing import Self  

class Node:
  def __init__(self: Self, points: list[Point], area: Area):
    self.points: list[Point] | None = None
    self.area: Area = area
    self.children: list[Node] | None = None #NW, NE, SW, SE
    #children[0] = NW
    #children[1] = NE
    #children[2] = SW
    #children[3] = SE
    self.insert(points)

  def insert(self: Self, points: list[Point], max_cardinality):
    if(len(self.points) + len(points) > max_cardinality):
      if(self.points is None):
        x_mid = (self.area.bottom_left.x + self.area.upper_right.x)/2
        y_mid = (self.area.bottom_left.y + self.area.upper_right.y)/2
        self.children = [
          Area(Point(self.area.bottom_left.x,y_mid), Point(x_mid, self.area.upper_right.y)), #NW
          Area(Point(x_mid,y_mid), Point(self.area.upper_right.x, self.area.upper_right.y)), #NE
          Area(Point(self.area.bottom_left.x,self.area.bottom_left.y), Point(x_mid, y_mid)), #SW
          Area(Point(x_mid,self.area.bottom_left.y), Point(self.area.upper_right.x, y_mid))  #SE
        ]
      
      P = [[]] * 4
      for point in points:
        if(point <= self.children[0].area.upper_right and point >= self.children[0].area.bottom_left): 
          P[0].append(point)
        elif(point > self.children[0].area.upper_right): 
          P[1].append(point)
        elif(point <= self.children[2].area.upper_right):
          P[2].append(point)
        else:
          P[3].append(point)
      
      for i in range(4):
        self.children[i].insert(P[i],max_cardinality)
    else:
      self.points.extend(points)

class Quadtree:
  def __init__(self, P: list[Point], max_cardinality: int):
    self.P = P
    self.max_cardinality = max_cardinality
    self.root = Node([], self._get_minimal_area(P))
    self.root.insert(P, max_cardinality)

  def _get_minimal_area(self, P: list[Point]):
    bottom_left, upper_right = Point(float('inf'), float('inf')), Point(float('-inf'), float('-inf'))
    for point in P:
      if bottom_left > point: bottom_left = point
      if upper_right < point: upper_right = point
    return Area(bottom_left,upper_right)

  def find_points_in_area(self: Self, area: Area):
    P = []
    self._find_points_in_area(area,P,self.root)
    
  def _find_points_in_area(self: Self, search_area: Area, P: list[Point], node: Node):
    if(search_area.contains_area(node.area)):
      if(node.points is None):
        for i in range(4):
          self._find_points_in_area(node.children[i], P)
      else:
        P.extend(node.points)
    elif(node.area.intersects_with_area(search_area)):
      if(node.points is None):
        for i in range(4):
          if(search_area.intersects_with_area(node.children[i])):
            self._find_points_in_area(search_area, P, node.children[i])
      else:
        for point in node.points:
          if(search_area.contains_point(point)):
            P.append(point)


def test():
  print('a')