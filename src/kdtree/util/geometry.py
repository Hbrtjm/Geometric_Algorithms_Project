from typing import Self, List

class Point:
    """
    Represents a K-dimensional point in space
    
    Arguments:

    """
    def __init__(self, x: float,y: float,z: float = None,higher_dimensions: List[float] = None):
        """
        Initializes a Point object with the given coordinates.

        Arguments:
        - x - The x-coordinate (required).
        - y - The y-coordinate (required).
        - z - The z-coordinate (default is None).
        - higher_dimensions (List[float], optional): Additional dimensions for K-dimensional points.

        """

        self.values = [x,y,z]
        if higher_dimensions:
            for element in higher_dimensions:
                self.values.append(element) # To avoid adding None or errors when using *higher_dimensions
        self.x = x
        self.y = y
        self.dimensions = len(self.values) if self.values[2] != None else 2

    def __str__(self: Self) -> str:
        """
        Returns a string representation of the point.
        """
        if self.values[2] != None:
            result = "("
            for index, element in enumerate(self.values):
                result = result + str(element) + ("," if index < self.dimensions-1 else ")")
            return result 
        return f"({self.x},{self.y})"

    def __eq__(self: Self, other: Self) -> bool:
        """
        Checks if two points are equal.

        Arguments:
        - other - The point to compare against.

        Returns:
        - Boolean if the points are equal or not
        """

        if other.dimensions != self.dimensions or other is None or not isinstance(other,type(self)):
            return False
        if self.values[2] != None:
            for index, value in enumerate(other.values):
                if self.values[index] != value:
                    return False
            return True
        else:
            return self.x == other.x and self.y == other.y
    
    def __lt__(self: Self, other: Self) -> bool:
        """
        Compares two points based on their x-coordinate.
        
        Arguments:
        - other - The point to compare against.

        """
        return self.x < other.x

    def __gt__(self: Self, other: Self) -> bool:
        """
        Compares two points based on their x-coordinate.

        Arguments:
        - other - The point to compare against.

        """
        return self.x > other.x
    
    def __iter__(self: Self) -> List[float]:
        """
        Allows iteration over the point's coordinates.
        """

        if self.values[2] != None:
            return self.values
        return [self.x,self.y]
    
    def __getitem__(self: Self,index: int) -> float:
        """
        Accesses a specific coordinate by index.

        Arguments:
        - index -  The index of the coordinate to retrieve.

        Returns:
        - value 
        """

        if self.values[2] != None:
            if index >= self.dimensions:
                raise ValueError("Point index out of range")
            return self.values[index]
        else:
            match index:
                case 0:
                    return self.x
                case 1:
                    return self.y
                case _:
                    raise ValueError("Point index out of range")
    
    def __setitem__(self: Self, index: int, value: float):
        """
        Modifies a specific coordinate by index.

        Arguments:
        - index - The index of the coordinate to modify.
        - value - The new value for the coordinate.

        """
        if self.values[2] != None:
            if index >= self.dimensions:
                raise ValueError("Point index out of range")
            self.values[index] = value
        else:
            match index:
                case 0:
                    self.x = value
                    self.values[0] = value
                case 1:
                    self.y = value
                    self.values[1] = value
                case _:
                    raise ValueError("Point index out of range")

              
# class Area:
#     """
#     Represents a rectangular area in 2D space.
    
#     Defined by two points: bottom-left and upper-right corners.
    
#     Attributes:
#         bottom_left: Point representing the bottom-left corner
#         upper_right: Point representing the upper-right corner
#     """
#     def __init__(self, bottom_left: Point, upper_right: Point) -> None:
#         self.bottom_left = bottom_left
#         self.upper_right = upper_right 
      
#     def __str__(self: Self) -> str:
#         return f"[{self.bottom_left}:{self.upper_right}]"
#     def __repr__(self: Self) -> str:
#         return f"[{self.bottom_left}:{self.upper_right}]"
  
#     def contains_area(self: Self, area: Area) -> bool:
#         """
#         Check if this area fully contains another area.
        
#         Arguments:
#             area: Area to check for containment
            
#         Returns:
#             True if the given area is completely contained within this area
#         """
#         return (
#             area.upper_right <= self.upper_right and 
#             area.bottom_left >= self.bottom_left
#         )
  
#     def intersects_with_area(self: Self, area: Area) -> bool:
#         """Check if this area intersects with another area.
        
#         Argsuments:
#             area: Area to check for intersection
            
#         Returns:
#             True if the areas intersect
#         """
#         return (
#             area.upper_right.x > self.bottom_left.x and 
#             area.bottom_left.x < self.upper_right.x and
#             area.upper_right.y > self.bottom_left.y and
#             area.bottom_left.y < self.upper_right.y
#         )
  
#     def contains_point(self: Self, point: Point) -> bool:
#         """Check if this area contains a point.
        
#         Arguments:
#             point: Point to check for containment
            
#         Returns:
#             True if the point lies within this area
#         """
#         return (
#             self.bottom_left.x <= point.x <= self.upper_right.x and
#             self.bottom_left.y <= point.y <= self.upper_right.y
#         )
