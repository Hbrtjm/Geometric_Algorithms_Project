from typing import Self
from __future__ import annotations

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
        return area.upper_right <= self.upper_right or area.bottom_left >= self.bottom_left