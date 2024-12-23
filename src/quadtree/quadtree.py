from __future__ import annotations
from .util.Geometry import Area, Point
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
        max_depth: Maximum allowed depth of the tree
        current_depth: Current depth of this node in the tree
    """
    def __init__(self: Self, area: Area, max_cardinality: int, max_depth: int = 100, 
                 current_depth: int = 0, points: list[Point] = []) -> None:
        self.points: list[Point] = []
        self.area: Area = area
        self.children: list[QuadtreeNode] = [[] for _ in range(4)]
        self.has_children: bool = False
        self.max_cardinality: int = max_cardinality
        self.max_depth: int = max_depth
        self.current_depth: int = current_depth
        self.insert(points)

    def insert(self: Self, points: list[Point]) -> None:
        """Insert a list of points into the quadtree node.
        
        Args:
            points: List of points to insert
        """
        if(len(self.points) + len(points) <= self.max_cardinality or self.current_depth == self.max_depth):
            self.points.extend(points)
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
        self.children = [QuadtreeNode(area, self.max_cardinality, self.max_depth, self.current_depth + 1) for area in areas]
        self.has_children = True
    
    def _distribute_points(self: Self, points: list[Point]) -> None:
        """Distribute points among child nodes.
        
        Args:
            points: List of points to distribute to appropriate child nodes
        """
        points.extend(self.points)
        self.points = []
        
        for point in points:
            for child in self.children:
                # The order of areas in area list takes care of proper edge-case handling
                if child.area.contains_point(point):
                    child.insert([point])
                    break
      

class Quadtree:
    """A quadtree data structure for efficient 2D point storage and retrieval.
    
    Attributes:
        max_cardinality: Maximum number of points in a node before subdivision
        max_depth: Maximum allowed depth of the tree
        root: Root node of the quadtree
    """
    def __init__(self, points: list[Point] = [], max_cardinality: int = 1, 
                 max_depth: int = 100) -> None:
        self.max_cardinality = max_cardinality
        self.max_depth = max_depth
        self.root = QuadtreeNode(self._get_minimal_area(points), max_cardinality, max_depth)
        self.root.insert(points)

    def _get_minimal_area(self, points: list[Point]) -> Area:
        """Calculate the minimal bounding area containing all points.
        
        Args:
            points: List of points to bound
            
        Returns:
            Area object representing the minimal bounding rectangle
        """
        xs, ys = zip(*[(p.x, p.y) for p in points])
        return Area(
            Point(min(xs), min(ys)),
            Point(max(xs), max(ys))
        )

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
            if(node.has_children):
                for child in node.children:
                    self._find_points_in_area(search_area, result, child)
            else:
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