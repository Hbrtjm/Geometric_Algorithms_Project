from __future__ import annotations
# Deleted . from util
from util.Geometry import Area, Point
from typing import Self

class QuadtreeNode:
    """A node in the quadtree data structure.
    
    Represents a region of 2D space that can contain points and be subdivided into four child nodes.
    
    Attributes:
        points: List of points contained in this node
        area: The rectangular area this node represents
        children: List of four child nodes (NW, NE, SW, SE)
        has_children: Whether this node has been subdivided
        max_cardinality: Maximum number of points before subdivision
    """
    def __init__(self: Self, max_cardinality: int, area: Area | None = None, points: list[Point] = []) -> None:
        self.points: set[Point] = set()
        self.area: Area | None = area
        self.children: list[QuadtreeNode] = [[] for _ in range(4)]
        self.has_children: bool = False
        self.max_cardinality: int = max_cardinality
        self.insert(points) 

    def insert(self: Self, points: set[Point]) -> None:
        """Insert a list of points into the quadtree node.
        
        Args:
            points: List of points to insert
        """
        
        if(self.area == None): self.area = self._get_minimal_area(points)
        self.points.update(points)
        if(len(self.points) <= self.max_cardinality):
            return

        if(not self.has_children):
            self._subdivide()
        self._distribute_points(points)

    def _subdivide(self: Self) -> None:
        """Create four child nodes by subdividing current area.
        
        Splits the current node's area into four equal quadrants and creates child nodes.
        """
        if self.has_children:
            return
        
        x_mid = (self.area.bottom_left.x + self.area.upper_right.x) / 2
        y_mid = (self.area.bottom_left.y + self.area.upper_right.y) / 2
        
        # Create areas for children (NW, NE, SW, SE)
        areas = [
            Area(Point(self.area.bottom_left.x, y_mid), Point(x_mid, self.area.upper_right.y)),  # NW
            Area(Point(x_mid, y_mid), self.area.upper_right),                                    # NE
            Area(self.area.bottom_left, Point(x_mid, y_mid)),                                    # SW
            Area(Point(x_mid, self.area.bottom_left.y), Point(self.area.upper_right.x, y_mid))   # SE
        ]
        
        # Initialize child nodes with incremented depth
        self.children = [QuadtreeNode(self.max_cardinality, area) for area in areas]
        self._distribute_points(self.points)
        self.has_children = True
    
    def _distribute_points(self: Self, points: list[Point]) -> None:
        """Distribute points among child nodes.
        
        Args:
            points: List of points to distribute to appropriate child nodes
        """
        for point in points:
            for child in self.children:
                # The order of areas in area list takes care of proper edge-case handling
                if child.area.contains_point(point):
                    child.insert([point])
                    break
    def _get_minimal_area(self, points: list[Point]) -> Area:
        """Calculate the minimal bounding area containing all points.
        
        Args:
            points: List of points to bound
            
        Returns:
            Area object representing the minimal bounding rectangle
        """
        if(len(points) == 0):
          return None
        xs, ys = zip(*[(p.x, p.y) for p in points])
        return Area(
            Point(min(xs), min(ys)),
            Point(max(xs), max(ys))
        )
      

class Quadtree:
    """A quadtree data structure for efficient 2D point lookup.
    
    Attributes:
        max_cardinality: Maximum number of points in a node before subdivision
        root: Root node of the quadtree
        base_area: A default 2D area, where points of Quadtree can be distributed. If not provided,
        Quadtree will determine it by selecting the minimal area spanned by points.
    """
    def __init__(self, points: list[Point] = [], max_cardinality: int = 1, default_area: Area=None) -> None:
        self.max_cardinality = max_cardinality
        self.root = QuadtreeNode(points=points, max_cardinality=max_cardinality, area=default_area)

    def find_points_in_area(self: Self, area: Area) -> list[Point]:
        """Find all points contained within the given area.
        
        Args:
            area: Area to search for points
            
        Returns:
            List of points contained within the area
        """
        result = []
        self._find_points_in_area(area,result,self.root)
        return result
    
    def _find_points_in_area(self: Self, search_area: Area, result: list[Point], 
                            node: QuadtreeNode) -> None:
        """Recursive helper function for finding points in an area.
        
        Args:
            search_area: Area to search within
            result: List to store found points
            node: Current node being searched
        """
        if(search_area.contains_area(node.area)):
            result.extend(node.points)
        
        elif(node.area.intersects_with_area(search_area)):
            if(node.has_children):
                for child in node.children:
                    if(search_area.intersects_with_area(child.area)):
                        self._find_points_in_area(search_area, result, child)
            else:
                result.extend(point for point in node.points if search_area.contains_point(point))
            
    def _print_all_points(self: Self, node: QuadtreeNode, result: list[Point]) -> None:
        """Recursively collect all points in the quadtree.
        
        Args:
            node: Current node to collect points from
            result: List to store collected points
        """
        if(node.has_children):
            for child in node.children:
                self._print_all_points(child, result)
        else:
            result.extend(node.points)
            
    def print_all_points(self: Self) -> None:
        """Print all points stored in the quadtree."""
        result = []
        self._print_all_points(self.root, result)
        print(len(result))
        print(result)