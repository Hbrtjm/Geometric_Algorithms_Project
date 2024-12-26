from matplotlib.patches import Rectangle
# Deleted quadtree. in the following import
from .quadtree import Quadtree, QuadtreeNode, Point, Area
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from typing import Optional

PLOT_TITLE_INTERACTIVE = 'QuadTree Visualization\nClick to add points or areas'

class QuadTreeVisualizer:
    def __init__(self, width=600, height=600):
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.fig.subplots_adjust(bottom=0.2, top=0.9)
        self.ax.set_title(PLOT_TITLE_INTERACTIVE)

        self.boundary = Area(Point(0, 0), Point(width, height))
        self.qt = Quadtree([], max_cardinality=1, default_area=self.boundary)
        
        # Setup the plot
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        
        # Connect event handlers
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        
        # Add buttons
        self.mode = 'point'
        self.area_points = []
        self.area_plt_objects = []
        self._add_buttons()
        
    def _add_buttons(self):
        """Add buttons to toggle between point and area insertion modes and clear the plot"""
        ax_point = plt.axes([0.7, 0.05, 0.1, 0.075])
        ax_area = plt.axes([0.81, 0.05, 0.1, 0.075])
        ax_clear = plt.axes([0.59, 0.05, 0.1, 0.075])
        
        self.btn_point = Button(ax_point, 'Point')
        self.btn_area = Button(ax_area, 'Area')
        self.btn_clear = Button(ax_clear, 'Clear')
        
        self.btn_point.on_clicked(self._set_point_mode)
        self.btn_area.on_clicked(self._set_area_mode)
        self.btn_clear.on_clicked(self._clear_plot)
        
    def _set_point_mode(self, event):
        """Set mode to point insertion"""
        self.mode = 'point'
        self.area_points = []
        
    def _set_area_mode(self, event):
        """Set mode to area insertion"""
        self.mode = 'area'
        self.area_points = []
        
    def _clear_plot(self, event):
        """Clear the plot without resetting the quadtree"""
        self.area_points = []
        self.area_plt_objects = []
        self.ax.clear()
        self.ax.set_xlim(0, self.boundary.upper_right.x)
        self.ax.set_ylim(0, self.boundary.upper_right.y)
        self.qt = Quadtree([], max_cardinality=1, default_area=self.boundary)
        self._draw_quadtree()
        self.ax.set_title(PLOT_TITLE_INTERACTIVE)
        plt.draw()
        
    def _draw_rectangle(self, area: Area, color='black', alpha=0.1, linewidth=1):
        """Draw a rectangle on the plot"""
        x = area.bottom_left.x
        y = area.bottom_left.y
        width = area.upper_right.x - area.bottom_left.x
        height = area.upper_right.y - area.bottom_left.y
        return self.ax.add_patch(Rectangle((x, y), width, height, fill=False, color=color, alpha=alpha, linewidth=linewidth))
    
    def _draw_point(self, point: Point, color='blue'):
        """Draw a point on the plot"""
        return self.ax.plot(point.x, point.y, '.', color=color, markersize=2)[0]
    
    def _draw_quadtree(self, node: Optional[QuadtreeNode] = None):
        """Recursively draw the quadtree"""
        if node is None:
            node = self.qt.root
            self.ax.clear()
            self.ax.set_xlim(0, self.boundary.upper_right.x)
            self.ax.set_ylim(0, self.boundary.upper_right.y)
        
        # Draw current node's boundary
        self._draw_rectangle(node.area)
        
        # Draw points in this node
        if(not node.has_children):
          for point in node.points:
              self._draw_point(point)
        
        # Recursively draw children
        if node.has_children:
            for child in node.children:
                self._draw_quadtree(child)
    
    def _on_click(self, event):
        """Handle mouse click events"""
        if event.inaxes != self.ax:
            return
        
        if self.mode == 'point':
            # Create and insert new point
            new_point = Point(event.xdata, event.ydata)
            self.qt.root.insert([new_point])
        elif self.mode == 'area':
            if(len(self.area_points) == 0):
              while(len(self.area_plt_objects) > 0):
                obj = self.area_plt_objects.pop()
                obj.remove()
            # Collect points for area definition
            area_point = Point(event.xdata, event.ydata)
            self.area_points.append(area_point)
            self.area_plt_objects.append(self._draw_point(area_point, color='red'))
            
            if len(self.area_points) == 2:
                # Create and visualize area
                bottom_left = Point(min(self.area_points[0].x, self.area_points[1].x), min(self.area_points[0].y, self.area_points[1].y))
                upper_right = Point(max(self.area_points[0].x, self.area_points[1].x), max(self.area_points[0].y, self.area_points[1].y))
                area = Area(bottom_left, upper_right)
                self.area_plt_objects.append(self._draw_rectangle(area, color='red', alpha=1))
                self.area_points = []
                
                points_in_area = self.qt.find_points_in_area(area)
                print('-----------------------------------------------------------------------')
                print('SELECTED POINTS:')
                if(len(points_in_area) == 0): 
                  print('No points selected')
                else:
                  for point in points_in_area:
                    self.area_plt_objects.append(self._draw_point(point, color='red'))
                    print(point)
                print('-----------------------------------------------------------------------')
            self.ax.set_title(PLOT_TITLE_INTERACTIVE)
            plt.draw()
            return
        
        # Redraw the quadtree
        self._draw_quadtree()
        self.ax.set_title('QuadTree Visualization\nClick to add points or areas')
        plt.draw()
    
    def show(self):
        """Display the visualization"""
        
        plt.show()
    
    @staticmethod
    def _draw_static_plot(qt: Quadtree, selected_area: Area = None):
        fig, ax = plt.subplots()
        
        ax.set_title('Quadtree Visualization')
        
        def draw_node(node: QuadtreeNode):
            # Draw the area of the node
            rect = Rectangle(
                (node.area.bottom_left.x, node.area.bottom_left.y),
                node.area.upper_right.x - node.area.bottom_left.x,
                node.area.upper_right.y - node.area.bottom_left.y,
                linewidth=1, edgecolor='black', facecolor='none'
            )
            ax.add_patch(rect)
            
            # Draw points in the node
            for point in node.points:
                ax.plot(point.x, point.y, '.', color='blue')
            
            # Recursively draw child nodes
            if node.has_children:
                for child in node.children:
                    draw_node(child)
        
        # Draw the quadtree
        draw_node(qt.root)
        
        # If selected_area is provided, draw it and mark points inside it with red
        if selected_area:
            rect = Rectangle(
                (selected_area.bottom_left.x, selected_area.bottom_left.y),
                selected_area.upper_right.x - selected_area.bottom_left.x,
                selected_area.upper_right.y - selected_area.bottom_left.y,
                linewidth=1, edgecolor='red', facecolor='none'
            )
            ax.add_patch(rect)
            
            points_in_area = qt.find_points_in_area(selected_area)
            for point in points_in_area:
                ax.plot(point.x, point.y, '.', color='red')
        
        ax.set_aspect('equal', 'box')  # Make the axes even
        plt.xlabel('X')
        plt.ylabel('Y')
        # plt.show()
        
    def draw_static_plot(qt: Quadtree, selected_area: Area = None):
        QuadTreeVisualizer._draw_static_plot(qt,selected_area)
        plt.show()
    
    def save_static_plot(qt: Quadtree, save_path:str, selected_area: Area = None):
        QuadTreeVisualizer._draw_static_plot(qt,selected_area)
        plt.savefig(save_path)

if __name__ == "__main__":
    # visualizer = QuadTreeVisualizer()
    # visualizer.show()
    import os
    points = [(7.972658514060723,2.9213051894416964), 
          (2.8401395213191707,2.3350141150011297), 
          (4.169765238132268,9.45195039297934), 
          (6.763021398609743,5.22074189912268), 
          (9.94449930511674,5.194687843068271), 
          (2.2456471549083212,8.97557406422351), 
          (7.040128595128703,3.156306135972465), 
          (1.1755180923817277,3.2991083286467218), 
          (1.6533865111246049,4.57215235411275), 
          (1.0566093659389786,0.5245294379309773)]
    P = [Point(point[0], point[1]) for point in points]
    Q = Quadtree(P,1)
    area = Area(Point(0,0), Point(5,5))
    QuadTreeVisualizer.draw_static_plot(Q,area)
    QuadTreeVisualizer.save_static_plot(Q,os.path.join('C:\\Users\\Paweł\\Desktop\\Geometric_Algorithms_Project\\data\\img\\test.png'),area)
    