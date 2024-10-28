import time
def dfs(PuzzleSolver):
        if(PuzzleSolver.initial_board == 12345678):
            return "Already Solved"
        if not PuzzleSolver.is_solvable(PuzzleSolver.initial_board):
            return "No Solution"

        frontier = [(PuzzleSolver.initial_board, 0)]
        explored = set()
        parents = {PuzzleSolver.initial_board: (None, None)}
        max_depth = 0

        start_time = time.time()
        while frontier:
            state, depth = frontier.pop()
            explored.add(state)
            max_depth = max(max_depth, depth)

            for child, move in PuzzleSolver.neighbors(state):
                if child not in [f[0] for f in frontier] and child not in explored:
                    frontier.append((child, depth+1))
                    parents[child] = (state, move)

                    if child == PuzzleSolver.target_state:
                        end_time = time.time()
                        path, moves = PuzzleSolver.construct_solution(parents, child)
                        return moves, len(path)-1, len(explored), max(max_depth, depth + 1), (end_time - start_time)
        return "No Solution"
