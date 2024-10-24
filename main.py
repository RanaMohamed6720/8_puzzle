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
        self.pieces = [i for i in range(0, 9)]
        self.space = 0
        for i in range(9):
            b = EmptyPiece(text=str(i)) if i == 0 else PuzzlePiece(text=str(i))
            b.bind(on_press=self.on_piece_move)
            self.add_widget(b)

    def on_piece_move(self, puzzle_piece):
        index = self.children[::-1].index(puzzle_piece)
        if self.can_move( self.space,index):
            self.swap_widgets(index, self.space)
            self.pieces[self.space], self.pieces[index] = self.pieces[index], self.pieces[self.space]
            self.space = index
            self.update_board()

    def can_move(self, piece1_index, piece2_index):
        if abs(piece1_index - piece2_index) == 1 or abs(piece1_index - piece2_index) == 3:
            return True
        return False

    def update_board(self):
        for i in range(9):
            self.children[(i - 8) * -1].text = str(self.pieces[i])

    def swap_widgets(self, index1, index2):
        if index1 == index2:
            return
        widget1 = self.children[(index1 - 8) * -1]
        widget2 = self.children[(index2 - 8) * -1]
        self.remove_widget(widget1)
        self.remove_widget(widget2)
        self.add_widget(widget1, (index2 - 8) * -1)
        self.add_widget(widget2, (index1 - 8) * -1)

    def set_board(self, values):
        self.pieces = values
        index_of_zero = self.pieces.index(0)
        self.swap_widgets(self.space, index_of_zero)
        self.space = index_of_zero
        self.update_board()

    def solve_puzzle(self, algorithm):
        solver = PuzzleSolver(self.pieces, self.space)
        if algorithm == "bfs":
            solution_path = solver.bfs_solver()
        elif algorithm == "dfs":
            solution_path = solver.dfs_solver()
        elif algorithm == "ids":
            solution_path = solver.ids_solver()
        elif algorithm == "a_star":
            solution_path = solver.a_star_solver()

        if solution_path:
            for state in solution_path:
                self.set_board(list(state))
                print(state)
        else:
            print("No solution found")


class PuzzleSolver:
    def __init__(self, initial_board, empty_index):
        self.initial_board = initial_board
        self.empty_index = empty_index
        self.target_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    def neighbors(self, state, empty_index):
        neighbors = []
        row, col = empty_index // 3, empty_index % 3

        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                neighbors.append((tuple(new_state), new_index))

        return neighbors

    def bfs_solver(self):
        zero_pos = self.initial_board.index(0)
        start_state = tuple(self.initial_board)
        queue = deque([(start_state, zero_pos)])
        visited = {start_state: None}

        while queue:
            current_state, current_zero_pos = queue.popleft()

            if current_state == self.target_state:
                return self.construct_solution(visited, current_state)

            for neighbor, new_zero_pos in self.neighbors(current_state, current_zero_pos):
                if neighbor not in visited:
                    visited[neighbor] = current_state
                    queue.append((neighbor, new_zero_pos))

        return None

    def dfs_solver(self):
        pass

    def ids_solver(self):
        pass

    def a_star_solver(self):
        pass

    def construct_solution(self, visited, final_state):
        path = []
        while final_state is not None:
            path.append(final_state)
            final_state = visited[final_state]
        return path[::-1]


class InputPositions(BoxLayout):
    def validate(self, layout):
        input_grid = layout.ids.input_grid
        values = []

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
                    if num in values:
                        self.show_popup("Duplicates not allowed.")
                        return
                    values.append(num)
                except ValueError:
                    self.show_popup("Invalid input. Please enter a number.")
                    return

        for child in self.parent.children:
            if isinstance(child, PuzzleGrid):
                puzzle_grid = child
                break
        puzzle_grid.set_board(values[::-1])

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
