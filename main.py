from kivy.uix.dropdown import ScrollView
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import BooleanProperty
import puzzleSolver


MAX_DEPTH = 100 # used with IDS

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
            solver = puzzleSolver.PuzzleSolver(self.pieces, self.board_str().index("0"))
            
            if algorithm == "bfs":
                result = solver.bfs_solver()
            elif algorithm == "dfs":
                result = solver.dfs_solver()
            elif algorithm == "ids":
                result = solver.ids_solver(MAX_DEPTH)
            elif algorithm == "manhattan_a_star":
                result = solver.a_star_solver('manhattan')
            elif algorithm == "euclidean_a_star":
                result = solver.a_star_solver('euclidean')
            
            if result == "Already Solved":
                self.show_results_popup("The puzzle is already solved.")
            elif result == "No Solution":
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
        text_input = TextInput(text=results_str,readonly=True,font_size=18, size_hint=(1,None),height=100000,multiline=True,  )
        scrollable_content = ScrollView(size_hint=(1,None),size=(780,680))
        scrollable_content.add_widget(text_input)
        self.results_popup = Popup(title='Puzzle Results',content=scrollable_content,size_hint=(None, None),size=(850, 750))


        
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
