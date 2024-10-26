from collections import deque
import heapq
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import time


class Wrapper(BoxLayout):
    pass


class PuzzlePiece(Button):
    pass


class EmptyPiece(Button):
    pass


class PuzzleGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.pieces = 12345678
        self.space = 0
        self.build_board()

    def board_str(self):
        return "0"+f"{self.pieces}" if(len(str(self.pieces))==8) else f"{self.pieces}"
    
    def build_board(self):
        pieces = self.board_str()
        for i in pieces:
            b = EmptyPiece(text=str(i)) if i == "0" else PuzzlePiece(text=str(i))
            b.bind(on_press=self.on_piece_move)
            self.add_widget(b)

    def on_piece_move(self, puzzle_piece):
        index = self.children[::-1].index(puzzle_piece)
        if self.can_move(self.space, index):
            self.pieces = self.swap_values(self.pieces, self.space, index)
            self.space = index
            self.update_board()

    def can_move(self, piece1_index, piece2_index):
        row1, col1 = (piece1_index // 3) ,(piece1_index % 3)
        row2, col2 = (piece2_index // 3) ,(piece2_index % 3)
        if (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1):
            return True
        return False

    def swap_values(self, board, index1, index2):
        board_str = "0"+f"{board}" if(len(str(board))==8) else f"{board}"
        if index1 != index2:
            if index1 > index2:  
                index1, index2 = index2, index1
            board_str = board_str[:index1] + board_str[index2] + board_str[index1 + 1:index2] + board_str[index1] + board_str[index2 + 1:]
        return int(board_str)

    def update_board(self):
        self.clear_widgets()
        self.build_board()
        

    def set_board(self, board):
        print(board)
        self.pieces = board
        self.space = self.board_str().index("0")
        self.update_board()

    def solve_puzzle(self, algorithm):
        solver = PuzzleSolver(self.pieces, self.board_str().index("0"))

        if algorithm == "bfs":
            result = solver.bfs_solver()
            if isinstance(result, str):
                print(result)
            else:
                actions, cost, nodes_expanded, search_depth, running_time = result
                print("actions:", actions)
                print("cost:", cost)
                print("nodes expanded:", nodes_expanded)
                print("search depth:", search_depth)
                print("running time:", running_time)
        elif algorithm == "dfs":
            result = solver.dfs_solver()
        elif algorithm == "ids":
            result = solver.ids_solver()
        elif algorithm == "a_star":
            result = solver.a_star_solver()





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
                neighbors.append((child,action))
        return neighbors

    def bfs_solver(self):
        if(self.initial_board == 12345678):
            return "Already Solved"
        frontier = deque([(self.initial_board, 1)])  # each state in the frontier has a state of the board , depth
        visited = set()
        visited.add(self.initial_board)
        nodes_expanded = 0
        max_depth = 0
        parents = {self.initial_board: (None, None)}
        start_time = time.time()

        while frontier:
            current_state, current_depth = frontier.popleft()
            nodes_expanded += 1
            max_depth = max(max_depth, current_depth)
            for neighbor, action in self.neighbors(current_state):
                if neighbor not in visited and neighbor not in frontier:
                    frontier.append((neighbor, current_depth + 1)) 
                    visited.add(neighbor)
                    parents[neighbor] = (current_state, action)
                    if int(neighbor) == self.target_state:
                        end_time = time.time()
                        path, actions = self.construct_solution(parents, neighbor)
                        cost = len(path) - 1  
                        return actions, cost, nodes_expanded, max_depth, (end_time - start_time)

        return "No solution"


    def dfs_solver(self):
        pass

    def ids_solver(self):
        pass

    def a_star_solver(self):
        pass

    def construct_solution(self, parents, final_state):
        path = []
        actions = []
        while final_state is not None:
            parent_state , action = parents[final_state]
            if(action is not None):
                actions.append(action)
            path.append(final_state)
            final_state = parent_state
        print(path)
        return path[::-1],actions[::-1]


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
