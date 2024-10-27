from collections import deque
from heapq import heappop
from heapq import heappush
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import time
from kivy.clock import Clock
from kivy.properties import BooleanProperty
import math

class Wrapper(BoxLayout):
    pass


class PuzzlePiece(Button):
    pass


class EmptyPiece(Button):
    pass


class PuzzleGrid(GridLayout):
    animating = BooleanProperty(False)
    results_popup =  Popup(title='Puzzle Results',content=Label(text='No results to be shown',), size_hint=(None, None), size=(800, 700))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.pieces = 12345678  #initial state of the puzzle
        self.space = 0          #initial position of the empty spot
        self.build_board()
    # method to convert the integer representation of the board to a string
    def board_str(self):
        return "0"+f"{self.pieces}" if(len(str(self.pieces))==8) else f"{self.pieces}"
    # method to build the puzzle board by creating a widget for each piece
    def build_board(self):
        pieces = self.board_str()
        for i in pieces:
            b = EmptyPiece(text=str(i)) if i == "0" else PuzzlePiece(text=str(i))
            b.bind(on_press=self.on_piece_move)
            self.add_widget(b)
    # handles the logic when a piece is clicked to be moved
    def on_piece_move(self, puzzle_piece):
        index = self.children[::-1].index(puzzle_piece)             #getting the index of the clicked piece
        if self.can_move(self.space, index):                        #check if the move is valid
            self.pieces = self.swap_values(self.space, index)       #swap the values in the board representation
            self.space = index                                      # update the position of the empty spot
            self.update_board()                                     # update the gui
    # method to check if a piece can be swapped with the space
    def can_move(self, piece1_index, piece2_index):
        row1, col1 = (piece1_index // 3) ,(piece1_index % 3)
        row2, col2 = (piece2_index // 3) ,(piece2_index % 3)
        # check if they are adjacent in the row or the column
        if (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1):
            return True
        return False
    # swaps the values of two pieces in the board state
    # by reconstructing the board string around the indices
    def swap_values(self, index1, index2):
        board_str = self.board_str()
        if index1 != index2:
            if index1 > index2:  
                index1, index2 = index2, index1
            board_str = board_str[:index1] + board_str[index2] + board_str[index1 + 1:index2] + board_str[index1] + board_str[index2 + 1:]
        return int(board_str)
    # updating the gui display of the board after a piece has moved
    # by clearing the widgets and rebuilding the board
    def update_board(self):
        self.clear_widgets()
        self.build_board()
        
    # method to set the board pieces according to the input boxes
    def set_board(self, board):
        print(board)
        self.pieces = board
        self.space = self.board_str().index("0")
        self.update_board()

    # method that handles the solution of the puzzle upon clicking on 
    # on of the algorithms buttons 
    def solve_puzzle(self, algorithm):
        if not self.animating:
            solver = PuzzleSolver(self.pieces, self.board_str().index("0"))
            
            if algorithm == "bfs":
                result = solver.bfs_solver()
            elif algorithm == "dfs":
                result = solver.dfs_solver()
            elif algorithm == "ids":
                result = solver.ids_solver()
            elif algorithm == "manhattan_a_star":
                result = solver.a_star_solver('manhattan')
            elif algorithm == "euclidean_a_star":
                result = solver.a_star_solver('euclidean')
            
            if result == "Already Solved":
                self.show_results_popup("The puzzle is already solved.")
            elif result == "No solution":
                self.show_results_popup("No solution exists for this puzzle.")
            else:
                actions, cost, nodes_expanded, search_depth, running_time = result
                actions_str = " -> ".join(actions)
                self.show_results_popup(
                    f"Actions: {actions_str}\n\n"
                    f"Cost: {cost}\n\n"
                    f"Nodes Expanded: {nodes_expanded}\n\n"
                    f"Search Depth: {search_depth}\n\n"
                    f"Running Time: {running_time:.6f} seconds"
                )
                
                self.solution_actions = actions
                self.animating = True
                self.move_step_by_step()


    def show_results_popup(self, results_str): 
        self.results_popup = Popup(title='Puzzle Results',content=Label(text=results_str,text_size=(380, None)), size_hint=(None, None), size=(800, 700))
        
    def show_results(self):
        self.results_popup.open()
    # method to visualize the solution on the board
    def move_step_by_step(self, *args):
        if self.solution_actions:
            action = self.solution_actions.pop(0)
            self.apply_move(action)
            # scheduling the rest of the actions after small delay
            Clock.schedule_once(self.move_step_by_step, 0.5)
        else:
            self.animating = False # displaying of the result is done
    # method to apply a specific action on the board
    def apply_move(self, action):
        space_index = self.space
        if action == "up":
            target_index = space_index - 3
        elif action == "down":
            target_index = space_index + 3
        elif action == "left":
            target_index = space_index - 1
        elif action == "right":
            target_index = space_index + 1
        else:
            return
        self.pieces = self.swap_values(space_index, target_index)
        self.space = target_index
        self.update_board()

    def stop_animation(self):
        self.solution_actions = []
        self.animating = False

    def reset_board(self):
        if not self.animating:
            self.set_board(12345678)




# class that contains algorithms implementation
class PuzzleSolver:
    def __init__(self, initial_board,space_index):
        self.initial_board = initial_board
        self.target_state = 12345678
        self.space = space_index
    #  get neighbors in a string is swapping the zero with character at 
    #  index -1 / index +1 / index -3 / index +3 considering the borders
    def neighbors(self, state):
        neighbors = []
        state_str = "0" + f"{state}" if(len(str(state))==8) else f"{state}"  
        zero_index = state_str.index("0")
        row, col = zero_index // 3, zero_index % 3
        movements = [(-1, 0,'up'), (0, 1,'right'), (0, -1,'left'), (1, 0,'down')]
        for dr , dc,action in movements:
            new_row , new_col = row + dr , col + dc

            if(0<= new_row < 3 and 0 <= new_col < 3):
                new_index = new_row * 3 + new_col
                num = state_str[new_index]
                index = zero_index
                if(index >= new_index):
                    index , new_index = new_index , index
                child = (
                    state_str[:index] +
                    state_str[new_index] +
                    state_str[index + 1:new_index] +
                    state_str[index] +
                    state_str[new_index + 1:]
                )
                neighbors.append((child, action, new_row, new_col, int(num)))
        return neighbors

    def bfs_solver(self):
        # check if the initial state is already the target
        if(self.initial_board == 12345678):
            return "Already Solved"
        frontier = deque([(self.initial_board, 1)])  # each state in the frontier has a state of the board , depth
        visited = set() 
        visited.add(self.initial_board) # mark the initial state as visited
        nodes_expanded = 0
        max_depth = 0
        parents = {self.initial_board: (None, None)} # parents dictionary to store the parent of a node and the actions that leads to it
        start_time = time.time() 

        while frontier:
            # 1- pop
            current_state, current_depth = frontier.popleft()
            nodes_expanded += 1
            max_depth = max(max_depth, current_depth)
            # 2- explore neighbors
            for neighbor, action, _, _, _ in self.neighbors(current_state):
                if neighbor not in visited and neighbor not in frontier:
                    frontier.append((neighbor, current_depth + 1)) 
                    visited.add(neighbor)
                    parents[neighbor] = (current_state, action)
                    # 3- check if it match the target state
                    if int(neighbor) == self.target_state:# target is reached and algorithm terminate
                        end_time = time.time() 
                        path, actions = self.construct_solution(parents, neighbor)
                        cost = len(path) - 1   # depth of the goal is the num. of steps to reach it -1 
                        return actions, cost, nodes_expanded, max_depth, (end_time - start_time)

        return "No solution" # if all nodes are explored then no solution for this puzzle


    def dfs_solver(self):
        pass

    def ids_solver(self):
        pass

    def a_star_solver(self, heuristic='euclidean'):
        if(self.initial_board == 12345678):
            return "Already Solved"
        frontier = []
        heappush(frontier, (0, 0, self.initial_board))

        explored = set()
        explored.add(self.initial_board)

        parent = ['left']
        expanded = 0
        start_time = time.time()

        while frontier:
            cost, cur_depth, state = heappop(frontier)

            if self.target_state == int(state):
                end_time = time.time()
                total_time = end_time - start_time
                return parent, cost, expanded, cur_depth, total_time

            expanded += 1

            for child, action, row, col, num in self.neighbors(state):
                if child not in explored and child not in frontier:
                    g = cur_depth + 1
                    h = self.Euclidean_Distance_Heuristic(row, col, num) if heuristic == 'euclidean' else self.Manhattan_Distance_Heuristic(row, col, num)
                    f = g + h
                    heappush(frontier, (f, g, child))
                    explored.add(child)

    def Manhattan_Distance_Heuristic(self, current_x, curretn_y, num):
        goal_x, goal_y = num // 3, num % 3
        return abs(current_x - goal_x) + abs(curretn_y - goal_y)

    def Euclidean_Distance_Heuristic(self, current_x, curretn_y, num):
        goal_x, goal_y = num // 3, num % 3
        return math.sqrt((current_x - goal_x) ** 2 + (curretn_y - goal_y) ** 2)
    # method to backtrack from the final state of the puzzle to the initial state to construct the solution path
    def construct_solution(self, parents, final_state):
        path = []
        actions = []
        while final_state is not None:
            # retrieve the parent and the action that led to this state from parents dictionary
            parent_state , action = parents[final_state]
            if(action is not None):
                actions.append(action)
            path.append(final_state)
            final_state = parent_state # moving a step back
        print(path)
        return path[::-1],actions[::-1] # reverse to start from the initial state

# class to handle setting the board through the input boxes
class InputPositions(BoxLayout):
    def validate(self, layout):
        input_grid = layout.ids.input_grid
        board_str = ""

        for widget in input_grid.children:
            if isinstance(widget, CustomInputField):
                value = widget.text.strip()
                if not value:
                    self.show_popup("Input cannot be empty.")
                    return
                try:
                    num = int(value)
                    if num < 0 or num > 8:
                        self.show_popup("Value must be between 0 and 8.")
                        return
                    if str(num) in board_str:
                        self.show_popup("Duplicates not allowed.")
                        return
                    board_str += str(num)
                except ValueError:
                    self.show_popup("Invalid input. Please enter a number.")
                    return
        board_str=board_str[::-1]
        board = int(board_str)
        for child in self.parent.children:
            if isinstance(child, PuzzleGrid):
                puzzle_grid = child
                break
        puzzle_grid.set_board(board)


    def show_popup(self, message):
        popup = Popup(title='Validation Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class CustomInputField(TextInput):
    pass


class InputGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        for i in range(9):
            b = CustomInputField()
            self.add_widget(b)


class PuzzleApp(App):
    def build(self):
        return Wrapper()


if __name__ == "__main__":
    PuzzleApp().run()
