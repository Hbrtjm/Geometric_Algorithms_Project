import matplotlib.pyplot as plt
from .kdtree import KDTree, Point, Node
from typing import Self, List
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button, TextBox


class KDTreeVisualizer:

    def __init__(self: Self, width: int = 600, height: int = 600):

        # Application attributes
        self.title = "Interaktywna wizualizacja KD-drzewa"
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.fig.subplots_adjust(bottom=0.2, top=0.9)
        self.ax.set_title(self.title)
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.bounds = [(0,width),(0,height)]
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Objects used for visualization
        self.treePlotObjects = []
        self.saveFilename = "points.txt"
        self.loadFilename = "points.txt"
        self.points = []
        self.rectangle = [(None,None), (None,None)]
        self.kdtree = KDTree()
        self.area_plt_objects = []
        
        # Initial state
        self.mode = 'point'
        self.add_widgets()
        
        plt.show()

    def rebuild_tree(self):
        """
        After each click it rebuilds the tree
        """
        self.kdtree = KDTree()
        self.kdtree.build_tree(self.points)
    def correct_rectangle(self):
        """
        Orders the rectangle by the given points, 
        so that the element at index 0 contains lower left point,
        and element at index 1 contains upper right point of the rectangle
        """
        bottom_left = Point(min(self.rectangle[0].x, self.rectangle[1].x), min(self.rectangle[0].y, self.rectangle[1].y))
        upper_right = Point(max(self.rectangle[0].x, self.rectangle[1].x), max(self.rectangle[0].y, self.rectangle[1].y))
        self.rectangle = [bottom_left, upper_right]
    
    def add_widgets(self: Self):
        """
        Add buttons and input fields to the GUI interface.

        Widgets:
        1. Point Mode Button - Activates point mode. When enabled, clicking on the plot area will place a point and add it to the data tree.
        2. Area Mode Button - Activates area mode. The function for this button is not fully described in the comment, but it likely enables selecting or defining areas on the plot.
        3. Clear Button - Clears all points and areas from the plot.
        4. Save to File Button - Saves points from the plot to a file. Filename is specified in the adjacent input field.
        5. Load from File Button - Loads points from a file into the plot. Filename is specified in the adjacent input field.
        6. Text Input Fields 
        - Save Filename Input: Specifies the filename to save the points (default: "punkty.txt").
        - Load Filename Input: Specifies the filename to load points from (default: "punkty.txt").
        """
        pointModeButtonPosition = plt.axes([0.7, 0.05, 0.1, 0.075])
        areaModeButtonPosition = plt.axes([0.81, 0.05, 0.1, 0.075])
        clearButtonPosition = plt.axes([0.59, 0.05, 0.1, 0.075])
        saveToFileButtonPosition = plt.axes([0.48, 0.05, 0.1, 0.075])
        saveToFileInputBoxPosition = plt.axes([0.37, 0.05, 0.1, 0.075])
        loadPointsFromFileButtonPosition = plt.axes([0.26, 0.05, 0.1, 0.075])
        loadPointsFromInputBoxPosition = plt.axes([0.15, 0.05, 0.1, 0.075])

        self.buttonAddPoints = Button(pointModeButtonPosition , 'Point')
        self.buttonAddArea = Button(areaModeButtonPosition, 'Area')
        self.buttonClear = Button(clearButtonPosition, 'Clear')
        self.buttonSavePoints = Button(saveToFileButtonPosition, 'Save')
        self.buttonLoadPoints = Button(loadPointsFromFileButtonPosition, 'Load')
        self.textBoxSaveFilename = TextBox(saveToFileInputBoxPosition, '', initial="punkty.txt")
        self.textBoxLoadFilename = TextBox(loadPointsFromInputBoxPosition, '', initial="punkty.txt")
        
        self.buttonSavePoints.on_clicked(self.save_points)
        self.buttonLoadPoints.on_clicked(self.load_points)
        self.buttonAddPoints.on_clicked(self.set_point_mode)
        self.buttonAddArea.on_clicked(self.set_area_mode)
        self.buttonClear.on_clicked(self.clear_plot)

    def update_save_filename(self: Self):
        self.saveFilename = self.textBoxSaveFilename.text_disp._text
    
    def update_load_filename(self: Self):
        self.loadFilename = self.textBoxLoadFilename.text_disp._text

    def set_point_mode(self: Self, event):
        """
        Set mode to point insertion
        """
        self.buttonAddPoints.color = 'green'
        self.buttonAddArea.color = 'lightgray'
        self.mode = 'point'
        self.rectangle = []
        
    def set_area_mode(self: Self, event):
        """
        Set mode to area insertion
        """
        self.buttonAddPoints.color = 'lightgray'
        self.buttonAddArea.color = 'green'
        self.mode = 'area'
        self.rectangle = []
    

    def clear_plot(self: Self, event):
        """
        Clear the plot
        """
        self.rectangle = []
        self.area_plt_objects = []
        self.points = []
        while(len(self.treePlotObjects) > 0):
            obj = self.treePlotObjects.pop()
            obj[0].remove()
        self.ax.clear()
        self.ax.set_xlim(*self.bounds[0])
        self.ax.set_ylim(*self.bounds[1])
        self.kdtree = KDTree()
        # self.plot_kdtree_splits(self.kdtree.root)
        self.ax.set_title(self.title)
        plt.draw()
        
    def draw_rectangle(self: Self, color='black', alpha=0.01, linewidth=1):
        """
        Draw a rectangle on the plot
        """
        x = self.rectangle[0].x
        y = self.rectangle[0].y
        width = self.rectangle[1].x - self.rectangle[0].x
        height = self.rectangle[1].y - self.rectangle[0].y
        return self.ax.add_patch(Rectangle((x, y), width, height, fill=False, color=color, alpha=alpha, linewidth=linewidth))
    
    def load_points(self: Self,event):
        """
        Loads points from the file. The filename is given in the loadFilename input box
        """
        self.update_load_filename()
        # print(self.loadFilename)
        self.clear_plot(None)
        self.points = []
        try:
            with open(self.loadFilename, "r") as f:
                for line in f:
                    x, y = map(float, line.strip().split(","))
                    self.points.append(Point(x, y))
        except FileNotFoundError:
            return
            # print("File not found!")
        self.kdtree = KDTree()
        for point in self.points:
            self.draw_point(point,size=4)
        self.kdtree.build_tree(self.points)
        self.plot_kdtree()
        self.ax.set_title('Interaktywna wizualizacja KD-drzewa')
        plt.draw()
    
    def save_points(self: Self,event):
        """
        Saves points to the file. The filename is given in the saveFilename input box
        """
        self.update_save_filename()
        with open(self.saveFilename, "w") as f:
            for point in self.points:
                f.write(f"{point[0]},{point[1]}\n")
        # print(f"Points saved to {self.saveFilename}")    

    def draw_point(self: Self, point: Point, color='black', size=2):
        """
        Draw a point on the plot
        """
        return self.ax.plot(point.x, point.y, '.', color=color, markersize=size,zorder=2)[0]
    
    def plot_kdtree(self):
        while(len(self.treePlotObjects) > 0):
            obj = self.treePlotObjects.pop()
            obj[0].remove()
        self.plot_kdtree_splits(self.kdtree.root, bounds=self.bounds)
        
    def plot_kdtree_splits(self, node, depth=0, bounds=None):
        """
        Recursively plot the splitting lines of a KDTree.
        Parameters:
            ax: The matplotlib Axes object to draw on.
            node: The current Node of the KDTree.
            depth: The current depth in the tree.
            bounds: The bounding box for the current region, in the form [(xmin, xmax), (ymin, ymax)].
        """
        if node is None or node.value is None:
            return
        if bounds is None:
            # Initialize bounds as infinite in both x and y dimensions
            bounds = [(-1, 1), (-1, 1)]
        axis = depth % 2
        x, y = node.value[0], node.value[1]
        line = None
        if axis == 0:  # Vertical line (split by x)
            line = self.ax.plot([x, x], [bounds[1][0], bounds[1][1]], color='blue', linestyle='--', linewidth=1,zorder=1)
            self.plot_kdtree_splits(node.left, depth + 1, [(bounds[0][0], x), bounds[1]])
            self.plot_kdtree_splits(node.right, depth + 1, [(x, bounds[0][1]), bounds[1]])
        else:  # Horizontal line (split by y)
            line = self.ax.plot([bounds[0][0], bounds[0][1]], [y, y], color='yellow', linestyle='--', linewidth=1,zorder=1)
            self.plot_kdtree_splits(node.left, depth + 1, [bounds[0], (bounds[1][0], y)])
            self.plot_kdtree_splits(node.right, depth + 1, [bounds[0], (y, bounds[1][1])])
        if line is not None:
            self.treePlotObjects.append(line)
        

    def in_bounds(self: Self,point: Point):
        """
        Checks if the click was in the bounds of canvas
        """
        return self.bounds[0][0] <=  point.x and point.x <= self.bounds[0][1] and self.bounds[1][0] <=  point.y and point.y <= self.bounds[1][1] 
    
    def on_click(self: Self, event):
        """
        Handle mouse click events
        """
        if event.inaxes != self.ax and event.xdata is None and event.ydata is None:
            return
        
        x, y = event.xdata, event.ydata
        
        if not self.in_bounds(Point(x,y)):
            # print(f"Point {Point(x,y)} is not in bounds")
            return
        if self.mode == 'point':
            # Create and insert new point
            newPoint = Point(x, y)
            self.draw_point(newPoint)
            self.points.append(newPoint)
            self.rebuild_tree()    
        elif self.mode == 'area':
            if(len(self.rectangle) == 0):
              while(len(self.area_plt_objects) > 0):
                obj = self.area_plt_objects.pop()
                obj.remove()
            # Collect points for area definition
            area_point = Point(x, y)
            self.rectangle.append(area_point)
            self.area_plt_objects.append(self.draw_point(area_point, color='red'))
            
            if len(self.rectangle) == 2:
                # Create and visualize area
                self.correct_rectangle()
                self.area_plt_objects.append(self.draw_rectangle(color='red', alpha=1))
                count, points_in_area = self.kdtree.get_points_in_rectangle(self.rectangle[0],self.rectangle[1])
                self.rectangle = []
                for point in points_in_area:
                    self.area_plt_objects.append(self.draw_point(point, color='red',size=6))
            self.ax.set_title(self.title)
            plt.draw()
            return
        
        # Redraw the quadtree
        self.plot_kdtree()
        self.ax.set_title('Interaktywna wizualizacja KD-drzewa')
        plt.draw()
    
    def show(self: Self):
        """
        Display the visualization
        """
        plt.show()
    
    @staticmethod
    def draw_plot(kdtree: KDTree, selectedArea: List[Point] = None, bounds=[(-1000, 1000), (-1000, 1000)]):
        fig, ax = plt.subplots()
        
        ax.set_title('KDTree Visualization')
            
        def plot_kdtree_splits(node, depth=0, bounds=None):
            """
            Recursively plot the splitting lines of a KDTree.
            Parameters:
                ax: The matplotlib Axes object to draw on.
                node: The current Node of the KDTree.
                depth: The current depth in the tree.
                bounds: The bounding box for the current region, in the form [(xmin, xmax), (ymin, ymax)].
            """
            if node is None or node.value is None:
                return
            if bounds is None:
                # Initialize bounds as infinite in both x and y dimensions
                bounds = [(-1, 1), (-1, 1)]
            nonlocal ax
            axis = depth % 2
            x, y = node.value[0], node.value[1]
            if axis == 0:  # Vertical line (split by x)
                ax.plot([x, x], [bounds[1][0], bounds[1][1]], color='blue', linestyle='--', linewidth=1,zorder=1)
                ax.plot(x, y, '.', color='blue', markersize=4,zorder=2)
                plot_kdtree_splits(node.left, depth + 1, [(bounds[0][0], x), bounds[1]])
                plot_kdtree_splits(node.right, depth + 1, [(x, bounds[0][1]), bounds[1]])
            else:  # Horizontal line (split by y)
                ax.plot([bounds[0][0], bounds[0][1]], [y, y], color='yellow', linestyle='--', linewidth=1,zorder=1)
                ax.plot(x, y, '.', color='blue', markersize=4,zorder=2)
                plot_kdtree_splits(node.left, depth + 1, [bounds[0], (bounds[1][0], y)])
                plot_kdtree_splits(node.right, depth + 1, [bounds[0], (y, bounds[1][1])])
        # If selected_area is provided, draw it and mark points inside it with red
        if selectedArea:
            rect = Rectangle(
                (selectedArea[0].x, selectedArea[0].y),
                selectedArea[1].x - selectedArea[0].x,
                selectedArea[1].y - selectedArea[0].y,
                linewidth=1, edgecolor='red', facecolor='none'
            )
            ax.add_patch(rect)
            
            count, points_in_area = kdtree.get_points_in_rectangle(*selectedArea)
            for point in points_in_area:
                ax.plot(point[0], point[1], '.', color='red', zorder=3)
        plot_kdtree_splits(kdtree.root,bounds= bounds)
        ax.set_aspect('equal', 'box')  # Make the axes even
        plt.xlabel('X')
        plt.ylabel('Y')

    @staticmethod
    def draw_static_plot(kdtree: KDTree, selectedArea: tuple[Point,Point] = None):
        KDTreeVisualizer.draw_plot(kdtree,selectedArea)
        plt.show()

    @staticmethod
    def save_static_plot(kdtree: KDTree, save_path:str, selectedArea: tuple[Point,Point] = None):
        KDTreeVisualizer.draw_plot(kdtree,selectedArea)
        plt.savefig(save_path)

def main():
    global limit, saveToFile, filename
    visualizer = KDTreeVisualizer()

if __name__ == "__main__":
    main()


