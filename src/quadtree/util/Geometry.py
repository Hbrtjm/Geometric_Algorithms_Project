from __future__ import annotations
from typing import Self

class Point:
    """Represents a 2D point with x and y coordinates.
    
    Attributes:
        x: x-coordinate
        y: y-coordinate
    """
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y 

    def __str__(self: Self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self):
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
        return [self.x,self.y]
    
    def __getitem__(self: Self,index: int) -> float:
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise ValueError("There is not such dimension")
    def __hash__(self):
        return hash((self.x,self.y))
              
class Area:
    """Represents a rectangular area in 2D space.
    
    Defined by two points: bottom-left and upper-right corners.
    
    Attributes:
        bottom_left: Point representing the bottom-left corner
        upper_right: Point representing the upper-right corner
    """
    def __init__(self, bottom_left: Point, upper_right: Point) -> None:
        self.bottom_left = bottom_left
        self.upper_right = upper_right 
      
    def __str__(self: Self) -> str:
        return f"[{self.bottom_left}:{self.upper_right}]"
    def __repr__(self: Self) -> str:
        return f"[{self.bottom_left}:{self.upper_right}]"
  
    def contains_area(self: Self, area: Area) -> bool:
        """Check if this area fully contains another area.
        
        Args:
            area: Area to check for containment
            
        Returns:
            True if the given area is completely contained within this area
        """
        return (
            area.upper_right <= self.upper_right and 
            area.bottom_left >= self.bottom_left
        )
  
    def intersects_with_area(self: Self, area: Area) -> bool:
        """Check if this area intersects with another area.
        
        Args:
            area: Area to check for intersection
            
        Returns:
            True if the areas intersect
        """
        return (
            area.upper_right.x > self.bottom_left.x and 
            area.bottom_left.x < self.upper_right.x and
            area.upper_right.y > self.bottom_left.y and
            area.bottom_left.y < self.upper_right.y
        )
  
    def contains_point(self: Self, point: Point) -> bool:
        """Check if this area contains a point.
        
        Args:
            point: Point to check for containment
            
        Returns:
            True if the point lies within this area
        """
        return (
            self.bottom_left.x <= point.x <= self.upper_right.x and
            self.bottom_left.y <= point.y <= self.upper_right.y
        )
