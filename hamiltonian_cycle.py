import pygame
import random

pygame.font.init()

X, Y = 50, 28
HALF_X = X//2
HALF_Y = Y//2
BLOCK_SIZE = 32
WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont('consolas', 20)

BGCOLOR = (130, 200, 255)
TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)
NODECOLOR = (210,105,30)
GRIDCOLOR = (150, 220, 255)

FPS = 40

clock = pygame.time.Clock()

class Node():
    def __init__(self, pos, number):
        self.pos = pos
        self.number = number

    def get_pos(self):
        return self.pos

    def get_number(self):
        return self.number  

def draw_grid():
    for x in range(1, X):
        pygame.draw.line(WIN, GRIDCOLOR, [x * BLOCK_SIZE, 0], [x * BLOCK_SIZE, Y * BLOCK_SIZE])
    for y in range(1, Y):
        pygame.draw.line(WIN, GRIDCOLOR, [0, y * BLOCK_SIZE], [X * BLOCK_SIZE, y * BLOCK_SIZE])

def draw_window(nodes, edges, points, cycle):
    WIN.fill(BGCOLOR)

    draw_grid()
    draw_edges(nodes, edges)
    draw_cycle(cycle)

    pygame.display.update()

def draw_cycle(points):
    prev = points[0]
    for point in points:
        pygame.draw.line(WIN, RED, [point[0] * BLOCK_SIZE + BLOCK_SIZE//2, point[1] * BLOCK_SIZE + BLOCK_SIZE//2], [prev[0] * BLOCK_SIZE + BLOCK_SIZE//2, prev[1] * BLOCK_SIZE + BLOCK_SIZE//2], 4)
        prev = point
        clock.tick(FPS)
        pygame.display.update()
    pygame.draw.line(WIN, RED, [points[0][0] * BLOCK_SIZE + BLOCK_SIZE//2, points[0][1] * BLOCK_SIZE + BLOCK_SIZE//2], [points[len(points)-1][0] * BLOCK_SIZE + BLOCK_SIZE//2, points[len(points)-1][1] * BLOCK_SIZE + BLOCK_SIZE//2], 4)

def draw_edges(nodes, edges):
    for edge in edges:
        for pos_x in range(0, HALF_X):
            for pos_y in range(0, HALF_Y):
                if (nodes[pos_x][pos_y].get_number() == edge[0][0]):
                    start = nodes[pos_x][pos_y].get_pos()
                if (nodes[pos_x][pos_y].get_number() == edge[0][1]):
                    end = nodes[pos_x][pos_y].get_pos()

        color = (100, 100, 100)

        pygame.draw.line(WIN, color, [start[0] * BLOCK_SIZE, start[1] * BLOCK_SIZE], [end[0] * BLOCK_SIZE, end[1] * BLOCK_SIZE ], 10)
        clock.tick(FPS)
        pygame.display.update()
    clock.tick(10)

def create_nodes():
    nodes = [[Node((x * 2 + 1, y * 2 + 1), x + y * HALF_X) for y in range(0, HALF_Y)] for x in range(0, HALF_X)]
    return nodes

def create_edges():
    edges = [[0 for y in range(0, HALF_Y * HALF_X)] for x in range(0, HALF_X * HALF_Y)]

    skiplist = [HALF_X * x for x in range(0, HALF_X)]
    for x in range(0, HALF_X * HALF_Y):
        for y in range(0, HALF_Y * HALF_X):
            if not (x == y):
                if (x + 1 == y and y not in skiplist): edges[x][y] = random.randint(1, 3)
                elif (x + HALF_X == y): edges[x][y] = random.randint(1, 3)

    return edges

def hamiltonian_cycle(nodes, edges):
    points = []
    for edge in edges:
        for pos_x in range(0, HALF_X):
            for pos_y in range(0, HALF_Y):
                if (nodes[pos_x][pos_y].get_number() == edge[0][0]):
                    start = nodes[pos_x][pos_y].get_pos()
                if (nodes[pos_x][pos_y].get_number() == edge[0][1]):
                    end = nodes[pos_x][pos_y].get_pos()
        points.append(start)
        points.append(((start[0]+end[0])//2, (start[1]+end[1])//2))
        points.append(end)

    cycle = [(0, 0)]

    curr = cycle[0]
    dir = (1, 0)

    while len(cycle) < X * Y:
        x = curr[0]
        y = curr[1]

        if dir == (1, 0): #right
            if ((x + dir[0], y + dir[1] + 1) in points and (x + 1, y) not in points):
                curr = (x + dir[0], y + dir[1])
            else:
                if ((x, y + 1) in points and (x + 1, y + 1) not in points):
                    dir = (0, 1)
                else:
                    dir = (0, -1)
        
        elif dir == (0, 1): #down
            if ((x + dir[0], y + dir[1]) in points and (x + dir[0] + 1, y + dir[1]) not in points):
                curr = (x + dir[0], y + dir[1])
            else:
                if ((x, y + 1) in points and (x + 1, y + 1) in points):
                    dir = (1, 0)
                else:
                    dir = (-1, 0)

        elif dir == (-1, 0): #left
            if ((x, y) in points and (x, y+1) not in points):
                curr = (x + dir[0], y + dir[1])
            else:
                if ((x, y + 1) not in points):
                    dir = (0, -1)
                else:
                    dir = (0, 1)

        elif dir == (0, -1): #up
            if ((x, y) not in points and (x + 1, y) in points):
                curr = (x + dir[0], y + dir[1])
            else:
                if ((x + 1, y) in points):
                    dir = (-1, 0)
                else:
                    dir = (1, 0)

        if curr not in cycle:
            cycle.append(curr)

    return points, cycle

def prims_algoritm(edges):
    clean_edges = []
    for x in range(0, HALF_X * HALF_Y):
        for y in range(0, HALF_Y * HALF_X):
            if not (edges[x][y] == 0):
                clean_edges.append(((x, y), edges[x][y]))
            
    visited = []
    unvisited = [x for x in range(HALF_X * HALF_Y)]
    curr = 0

    final_edges = []
    while len(unvisited) > 0:
        visited.append(curr)

        for number in unvisited:
            if number in visited:
                unvisited.remove(number)

        my_edges = []
        for edge in clean_edges:
            if ((edge[0][0] in visited or edge[0][1] in visited) and not (edge[0][0] in visited and edge[0][1] in visited)):
                my_edges.append(edge)

        min_edge = ((-1, -1), 999)

        for edge in my_edges:
            if (edge[1] < min_edge[1]):
                min_edge = edge
        
        if len(unvisited) == 0:
            break

        final_edges.append(min_edge)

        if min_edge[0][0] == -1:
            curr = unvisited[0]
        else:
            if (min_edge[0][1] in visited):
                curr = min_edge[0][0]
            else:
                curr = min_edge[0][1]

    return final_edges

def main():
    pygame.display.set_caption("Hamiltonian Cycle")

    nodes = create_nodes()
    edges = create_edges()

    final_edges = prims_algoritm(edges)
    points, cycle = hamiltonian_cycle(nodes, final_edges)

    draw_window(nodes, final_edges, points, cycle)

    main()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main()