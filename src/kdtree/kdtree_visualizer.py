import matplotlib.pyplot as plt
from kdtree import KDTree
import numpy as np
from matplotlib.widgets import Button

# TODO:
# Write all of the descriptions and comments

limit = 4
points = []
fig, ax = plt.subplots(figsize=(6,6))
fig.subplots_adjust(bottom=0.2, top=0.9)
saveToFile = False
filename = "wyniki.txt"
enterSquare = False
tree = KDTree()
lowerOrUpper = 0
drawRectangle = False
rectangle = [(None,None),(None,None)]

def update_plot():
    global limit, points, enterSquare, drawRectangle, tree, ax
    ax.clear()
    ax.set_title("Wprowadź punkty za pomocą myszki klikając na obszar")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_navigate(False)
    x_range = (-1, 1)
    y_range = (-1, 1)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    triangulation_result = []
    if len(points) != 0:
        x_coords, y_coords = zip(*points)
        ax.scatter(x_coords, y_coords, color="blue", s=5, label="Wprowadzone punkty")
    
    n = len(points)  
    if n == limit and not enterSquare:
        enterSquare = True
        tree.build_tree(points)
        if triangulation_result != []:    
            with open(filename,'w') as file:
                file.write('TODO') # ================================ TODO ================================
                file.close()
    if drawRectangle:
        # Display the rectangle
        lowerX, lowerY = rectangle[0]
        upperX, upperY = rectangle[1]
        rectangleX = [lowerX,lowerX,upperX,upperX]
        rectangleY = [upperY,lowerY,lowerY,upperY]
        ax.fill(rectangleX,rectangleY,'g',alpha=0.2)
        print("Rectangle added")

        # Calculate the points that are inside
        count, inside_points = tree.get_points_in_rectangle(rectangle[0],rectangle[1])
        if count > 0:
            x_coords, y_coords = zip(*inside_points)
            # Show them
            ax.scatter(x_coords, y_coords, color="red", zorder=4, s=5, label="Punkty wewnątrz prostokąta")
    if n == limit:
        # Draw the lines
        plot_kdtree_splits(tree.root)
    print("Frame updated")

    ax.legend()
    plt.draw()


def correct_rectangle():
    global rectangle
    lowerCopy = rectangle[0]
    rectangle[0] = (min(rectangle[0][0],rectangle[1][0]),min(rectangle[0][1],rectangle[1][1]))
    rectangle[1] = (max(lowerCopy[0],rectangle[1][0]),max(lowerCopy[1],rectangle[1][1]))


def onclick(event):
    global points, rectangle, enterSquare, lowerOrUpper, drawRectangle
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        if not enterSquare:
            points.append((x, y))
            update_plot()
        else: 
            rectangle[lowerOrUpper] = ((x,y))
            lowerOrUpper = (lowerOrUpper + 1) % 2
            if rectangle[1] != (None,None):
                drawRectangle = True
                correct_rectangle()
                update_plot()

def main():
    global limit, saveToFile, filename
    # saveToFileString = input("Czy wpisać wynik do pliku (1 - tak, w przeciwnym wypadku nie): ")
    # saveToFile = saveToFileString == '1'
    # if saveToFile:
    #     potential_filename = input("Proszę podać nazwę pliku (podstawowa nazwa to wyniki.txt): ")
    #     if potential_filename:
    #         filename = potential_filename
    limit_string = input("Ile punktów chcesz wprowadzić: ")
    if limit_string.isnumeric():
        limit = int(limit_string)
    fig.canvas.mpl_connect("button_press_event", onclick)
    update_plot()

    clear_ax = plt.axes([0.7, 0.05, 0.1, 0.075])  # [left, bottom, width, height]
    save_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    load_ax = plt.axes([0.59, 0.05, 0.1, 0.075])
    clear_button = Button(clear_ax, "Clear Points")
    save_button = Button(save_ax, "Save Points")
    load_button = Button(load_ax, "Load Points")

    # Connect button clicks to their respective functions
    clear_button.on_clicked(clear_points)
    save_button.on_clicked(save_points)
    load_button.on_clicked(load_points)
    plt.show()


def plot_kdtree_splits(node, depth=0, bounds=None):
    global ax
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
    if axis == 0:  # Vertical line (split by x)
        print(f"Plotting vertical {node.value} {x} {x}")
        ax.plot([x, x], [bounds[1][0], bounds[1][1]], color='blue', linestyle='--', linewidth=1)
        plot_kdtree_splits(node.left, depth + 1, [(bounds[0][0], x), bounds[1]])
        plot_kdtree_splits(node.right, depth + 1, [(x, bounds[0][1]), bounds[1]])
    else:  # Horizontal line (split by y)
        print(f"Plotting horizontal {node.value} {x} {x}")
        ax.plot([bounds[0][0], bounds[0][1]], [y, y], color='yellow', linestyle='--', linewidth=1)
        plot_kdtree_splits(node.left, depth + 1, [bounds[0], (bounds[1][0], y)])
        plot_kdtree_splits(node.right, depth + 1, [bounds[0], (y, bounds[1][1])])


def clear_points(event):
    global points, ax, rectangle, drawRectangle, tree, enterSquare
    points = []
    tree.root = None
    drawRectangle = False
    rectangle = [(None,None),(None,None)]
    enterSquare = False
    ax.clear()
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_aspect('equal')
    plt.draw()

def save_points(event):
    global points
    with open("points.txt", "w") as f:
        for point in points:
            f.write(f"{point[0]},{point[1]}\n")
    print("Points saved to points.txt")

def load_points(event):
    global points, ax
    points = []
    try:
        with open("points.txt", "r") as f:
            for line in f:
                x, y = map(float, line.strip().split(","))
                points.append((x, y))
    except FileNotFoundError:
        print("File not found!")
    update_plot()


if __name__ == "__main__":
    main()
