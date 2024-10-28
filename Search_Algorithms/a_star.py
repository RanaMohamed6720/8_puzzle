from heapq import heappop
from heapq import heappush
import math
import time
def a_star(PuzzleSolver, heuristic='euclidean'):
    if(PuzzleSolver.initial_board == 12345678):
        return "Already Solved"
    if not PuzzleSolver.is_solvable(PuzzleSolver.initial_board):
        return "No Solution"

    frontier = []
    heappush(frontier, (0, 0, PuzzleSolver.initial_board))

    explored = set()
    explored.add(PuzzleSolver.initial_board)

    parents = {PuzzleSolver.initial_board: (None, None)}
    expanded = 0
    start_time = time.time()
    max_depth = 0

    while frontier:
        _, cur_depth, state = heappop(frontier)
        max_depth = max(max_depth, cur_depth)
        expanded += 1

        for child, action in PuzzleSolver.neighbors(state):
            if child not in explored and child not in frontier:
                g = cur_depth + 1
                h = Euclidean_Distance_Heuristic(child) if heuristic == 'euclidean' else Manhattan_Distance_Heuristic(child)
                f = g + h
                parents[child] = (state, action)
                heappush(frontier, (f, g, child))
                explored.add(child)
            if PuzzleSolver.target_state == int(child):
                end_time = time.time()
                total_time = end_time - start_time
                path, actions = PuzzleSolver.construct_solution(parents, child)
                cost = len(path) - 1   # depth of the goal is the num. of steps to reach it -1
                return actions, cost, expanded, max(max_depth, cur_depth + 1), total_time

def Manhattan_Distance_Heuristic(grid):
    manhattan = 0
    i = 0
    while i < len(grid):
        if grid[i] == '0':
            i += 1
            continue
        current_x, current_y = i // 3, i % 3
        goal_x, goal_y = int(grid[i]) // 3, int(grid[i]) % 3
        manhattan += abs(current_x - goal_x) + abs(current_y - goal_y)
        i += 1
    return manhattan

def Euclidean_Distance_Heuristic(grid):
    euclidean = 0
    i = 0
    while i < len(grid):
        if grid[i] == '0':
            i += 1
            continue
        current_x, current_y = i // 3, i % 3
        goal_x, goal_y = int(grid[i]) // 3, int(grid[i]) % 3
        euclidean += math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2)
        i += 1
    return euclidean