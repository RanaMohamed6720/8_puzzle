

from heapq import heappop
from heapq import heappush
from kivy.metrics import dp
import time
import math
from Search_Algorithms.bfs import bfs
from Search_Algorithms.dfs import dfs
from Search_Algorithms.ids import ids
from Search_Algorithms.a_star import a_star

class PuzzleSolver:
    def __init__(self, initial_board,space_index):
        self.initial_board = initial_board
        self.target_state = 12345678
        self.space = space_index

    def bfs_solver(self):
        return bfs(self)
      

    def dfs_solver(self):
       return dfs(self)
    
    def ids_solver(self,max_depth):
        return ids(self,max_depth)


    def a_star_solver(self, heuristic='euclidean'):
        return a_star(self,heuristic='euclidean')
    
    #-------------------------------- Utility Functions -------------------------------------------------------

     # counting number of inversions in the initial state to check if it is solvable
    @staticmethod
    def count_inversions(state):
        str_state = str(state).replace('0', '')  # ignore the empty tile
        inversions = 0
        for i in range(len(str_state)):
            for j in range(i + 1, len(str_state)):
                if str_state[i] > str_state[j]:
                    inversions += 1
        return inversions

    # checking if the initial state is solvable
    # solvable if the number of inversions is even, otherwise it is unsolvable
    @staticmethod
    def is_solvable(state):
        inversions = PuzzleSolver.count_inversions(state)
        return inversions % 2 == 0

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
                child_int = int(child)
                neighbors.append((child_int, action))
        return neighbors



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