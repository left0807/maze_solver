import random
from collections import deque
import os
import time
from turtle import Turtle

height = 15
width = 15
maze = [['#' for y in range(height)] for x in range(width)]
visible = [[' ' for y in range(height)] for x in range(width)]

def print_maze():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*[" ".join(row) for row in visible], sep="\n")
    time.sleep(0.05)


def dfs_build():
    stack = [(1, 0)]
    
    while stack:
        #print_maze();

        x, y = stack[-1]
        maze[x][y] = ' '  # Mark current cell as empty
        
        # Create list of unvisited neighbors
        neighbors = []
        if x > 1 and maze[x-2][y] == '#':
            neighbors.append((x-2, y))
        if y > 1 and maze[x][y-2] == '#':
            neighbors.append((x, y-2))
        if x < width-2 and maze[x+2][y] == '#':
            neighbors.append((x+2, y))
        if y < height-2 and maze[x][y+2] == '#':
            neighbors.append((x, y+2))
        
        if neighbors:
            nx, ny = random.choice(neighbors)
            mx, my = (x+nx)//2, (y+ny)//2
            maze[mx][my] = ' '  # Mark wall between current and next cell as empty
            stack.append((nx, ny))  # Add next cell to stack
        else:
            stack.pop()  # Backtrack if no unvisited neighbors
    maze[height-2][width-1] = ' '

def kruskal_build():
    # Initialize maze grid with all walls    
    # Create list of wall cells and shuffle it
    walls = []
    for x in range(1, width-1, 2):
        for y in range(1, height-1, 2):
            if x < width-2:
                walls.append(((x, y), (x+2, y)))
            if y < height-2:
                walls.append(((x, y), (x, y+2)))
    random.shuffle(walls)
    
    # Create list of disjoint sets (each cell is its own set)
    sets = [[(x, y)] for x in range(width) for y in range(height)]
    
    for (x1, y1), (x2, y2) in walls:
        # Find the sets containing the two cells
        set1 = [s for s in sets if (x1, y1) in s][0]
        set2 = [s for s in sets if (x2, y2) in s][0]
        
        if set1 != set2:
            # Merge the two sets and carve a path between the two cells
            set1.extend(set2)
            sets.remove(set2)
            mx, my = (x1+x2)//2, (y1+y2)//2
            maze[mx][my] = ' '
            #print_maze()
        
def dfs_solve(start, end):
    stack = [start]

    while stack:
        pos = stack.pop()

        maze[pos[0]][pos[1]] = '@'
        visible[pos[0]][pos[1]] = '@'
        print_maze()

        found = False

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height: visible[new_pos[0]][new_pos[1]] = maze[new_pos[0]][new_pos[1]]
            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height and maze[new_pos[0]][new_pos[1]] == ' ':
                stack.append((new_pos))
                found = True;
        
        maze[pos[0]][pos[1]] = '.'
        visible[pos[0]][pos[1]] = '.'
        
            

    return None

def bfs_solve(start, end):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        pos, path = queue.popleft()
        visible[pos[0]][pos[1]] = '+'
        print_maze()
        if pos == end:
            return path + [pos]
        if pos in visited:
            continue
        visited.add(pos)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height and visible[new_pos[0]][new_pos[1]] != '#' and new_pos not in visited:
                queue.append((new_pos, path + [pos]))
    return None

# Call the BFS algorithm to find the shortest path

if __name__ == "__main__":
    dfs_build();
    end = (height-2, width-1)
    dfs_solve((0, 0), end)
    for pos in bfs_solve((0, 0), end):
        visible[pos[0]][pos[1]] = 'a'
        print_maze()
    
