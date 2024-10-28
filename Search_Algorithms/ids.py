import time
def dls(PuzzleSolver, state, goal_state, depth_limit):
        frontier = [(str(state), 0)]
        explored = {}
        parents = {str(state): (None, None)}
        max_depth = 0
        current_state = 0
        while frontier:
            current_state, depth = frontier.pop()

            explored[current_state] = depth
            max_depth = max(max_depth, depth)

            if int(current_state) == goal_state:
                path, moves = PuzzleSolver.construct_solution(parents, current_state)
                return moves, len(path)-1, len(explored), max_depth

            if depth < depth_limit:
                for child, move in PuzzleSolver.neighbors(current_state):
                    if not any(child == f[0] for f in frontier) and (child not in explored or depth + 1 < explored[child]):
                        frontier.append((child, depth + 1))
                        parents[child] = (current_state, move)
        return "No Solution"


def ids(PuzzleSolver, max_depth):
    if(PuzzleSolver.initial_board == 12345678):
        return "Already Solved"
    if not PuzzleSolver.is_solvable(PuzzleSolver.initial_board):
        return "No Solution"

    start_time = time.time()
    for depth_limit in range(max_depth):
        result = dls(PuzzleSolver, PuzzleSolver.initial_board, PuzzleSolver.target_state, depth_limit)
        end_time = time.time()
        if result != "No Solution":
            actions, cost, nodesExpanded, depth = result
            return actions, cost, nodesExpanded, depth, (end_time - start_time)
    return result