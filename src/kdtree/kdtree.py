from typing import Self, List
# from kdtreeutil import partition_array
import numpy as np
from .util.geometry import Point
class Node:
    """
    Tree node class
    Artibutes:
        value - stores a value of node
        left - pointer to the left node on the tree
        right - pointer to the right node on the tree
    
    """
    def __init__(self: Self,value: tuple=None):
        self.value = value
        self.left = None
        self.right = None
    def __str__(self: Self) -> str:
        return str(self.value)

class KDTree:
    """
    KDTree data structure that holds given points in a binary tree. The dimension can be adjusted, however currently it's used for 2-D application.
    On the first level it takes the median point by the x-coordinate, on the second it takes the median point by y-coordinate, loops back to the first coordinate 
    when it runs out of dimensions
    """
    def __init__(self: Self, K=2):
        self.root = None
        self.k = K
    
    def build_tree(self: Self, array: List[Point], depth: int=0) -> None:
        """
        Build the KDTree from the given array of points.
        Parameters:
        TODO
        """
        def _build_tree(array: List[Point], depth: int) -> Node:
            if not array:
                return None
            if len(array) == 1:
                return Node(array[0])

            dimension = depth % self.k 
            array.sort(key=lambda point: point[dimension])
            median_index = len(array) // 2
            
            # L,R,pivot = partition_array(array,dimension)
            # # # print(f"Picked pivot {pivot} and left {L} right {R}")
            # current = Node(pivot)
            # current.left = _build_tree(L, depth + 1)
            # current.right = _build_tree(R, depth + 1)

            current = Node(array[median_index])

            current.left = _build_tree(array[:median_index], depth + 1)
            current.right = _build_tree(array[median_index + 1:], depth + 1)

            return current

        self.root = _build_tree(array, depth)
    
    def insert_point(self: Self, point: Point):
        
        def insertRec(node: Node, point: Point, depth: int = 0):
            
            if not node:
                return Node(point)

            cd = depth % self.k

            if point[cd] < node.value[cd]:
                node.left = insertRec(node.left, point, depth + 1)
            else:
                node.right = insertRec(node.right, point, depth + 1)

            return node
        
        self.root = insertRec(self.root, point, 0)

    def copyPoint(self: Self,p1: Point, p2: Point):
        """
        Writes values from one point to another

        """
        for i in range(self.k):
            p1[i] = p2[i]
    
    def min_value_node(self: Self,node: Node):
        """
        
        """
        currentNode = node
        while currentNode.left:
            currentNode = currentNode.left
        return currentNode
    
    def delete_node_rec(self: Self, node: Node, point: Point, depth: int):
        """
        """
        if not node:
            return None
    
        dimension = depth % self.k
        if point[dimension] < node.value[dimension]:
            node.left = self.delete_node_rec(node.left, point, depth + 1)
        elif point[dimension] > node.value[dimension]:
            node.right = self.delete_node_rec(node.right, point, depth + 1)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                temp: Node = self.min_value_node(node.right)
                self.copyPoint(node.value, temp.value)
                node.right = self.delete_node_rec(node.right, temp.value, depth + 1)
        return node
    
    def delete_point(self: Self, point: Point):
        """
        Deletes node using recursive function defined above
        Arguments:
        node - a starting node
        point - a point value to be deleted
        """
        self.node = self.delete_node_rec(self.root, point, 0)
    
    def bst_to_list(self: Self):
        """
        Converts the whole tree int an array of form [left child]<-[parent]->[right child]
        """
        def transform(current: Node) -> List[Point]:
            if(current == None):
                return []
            return transform(current.left) + ([current.value] if current.value != None else [])   + transform(current.right)
        return transform(self.root)
    
    def get_points_in_rectangle(self: Self, lowerLeftPoint: Point, upperRightPoint: Point) -> tuple[int,List[Point]]:
        """
        Searches the given area and calculates how many and what points are in the given region in O(P) time, where P is the amounts of points in the rectangle
        On average this time would be O(h), where h is the height of the tree, where h = log(n), where n is the amount of all points
        Parameters:
            lowerLeftPoint - the lower-left point of the rectangle
            upperRightPoint - the upper-right point of the rectangle
        """
        count = 0
        points = []
        def inside(checked: Point):
            for i in range(self.k):
                if checked[i] < lowerLeftPoint[i] or checked[i] > upperRightPoint[i]:
                    return False
            return True  
        def recursive(current: Node, depth: int=0):
            if current is None:
                return
            nonlocal count, points
            left_side = current.value[depth%self.k] >= lowerLeftPoint[depth%self.k]
            right_side = current.value[depth%self.k] <= upperRightPoint[depth%self.k]
            if left_side and right_side and inside(current.value):
                count += 1
                points.append(current.value)
            if left_side:
                recursive(current.left,depth+1)
            if right_side:
                recursive(current.right,depth+1)
        recursive(self.root)
        return count, points
