from collections import deque
import time

def bfs(PuzzleSolver):
    # check if the initial state is already the target
    if(PuzzleSolver.initial_board == 12345678):
        return "Already Solved"
    if not PuzzleSolver.is_solvable(PuzzleSolver.initial_board):
        return "No Solution"
    frontier = deque([(PuzzleSolver.initial_board, 1)])  # each state in the frontier has a state of the board , depth
    visited = set() 
    visited.add(PuzzleSolver.initial_board) # mark the initial state as visited
    nodes_expanded = 0
    max_depth = 0
    parents = {PuzzleSolver.initial_board: (None, None)} # parents dictionary to store the parent of a node and the actions that leads to it
    start_time = time.time() 

    while frontier:
        # 1- pop
        current_state, current_depth = frontier.popleft()
        nodes_expanded += 1
        max_depth = max(max_depth, current_depth)
        # 2- explore neighbors
        for neighbor, action in PuzzleSolver.neighbors(current_state):
            if neighbor not in visited and neighbor not in [state for state, _ in frontier]:
                frontier.append((neighbor, current_depth + 1)) 
                visited.add(neighbor)
                parents[neighbor] = (current_state, action)
                # 3- check if it match the target state
                if int(neighbor) == PuzzleSolver.target_state:# target is reached and algorithm terminate
                    end_time = time.time() 
                    path, actions = PuzzleSolver.construct_solution(parents, neighbor)
                    cost = len(path) - 1   # depth of the goal is the num. of steps to reach it -1 
                    return actions, cost, nodes_expanded, max_depth, (end_time - start_time)

    return "No Solution" # if all nodes are explored then no solution for this puzzle