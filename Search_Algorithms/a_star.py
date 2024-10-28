from heapq import heappop
from heapq import heappush
import math
import time
def to_str(grid):
     return '0' + f'{grid}' if(len(str(grid))==8) else f'{grid}'
def a_star(PuzzleSolver, heuristic='euclidean'):
    if(PuzzleSolver.initial_board == 12345678):
        return "Already Solved"
    if not PuzzleSolver.is_solvable(PuzzleSolver.initial_board):
        return "No Solution"

    frontier = []
    heappush(frontier, (0, 0, PuzzleSolver.initial_board))

    explored = set()

    parents = {PuzzleSolver.initial_board: (None, None)}
    expanded = 0
    start_time = time.time()
    max_depth = 0

    while frontier:
        cost, cur_depth, state = heappop(frontier)
        max_depth = max(max_depth, cur_depth)

        explored.add(state)
        expanded += 1

        if PuzzleSolver.target_state == state:
                    end_time = time.time()
                    total_time = end_time - start_time
                    path, actions = PuzzleSolver.construct_solution(parents, state)
                    return actions, cost, expanded, max_depth, total_time

        for child, action in PuzzleSolver.neighbors(state):
            if child not in explored and not any(child == f[-1] for f in frontier):
                g = cur_depth + 1
                h = Euclidean_Distance_Heuristic(to_str(child)) if heuristic == 'euclidean' else Manhattan_Distance_Heuristic(to_str(child))
                f = g + h
                parents[child] = (state, action)
                heappush(frontier, (f, g, child))


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