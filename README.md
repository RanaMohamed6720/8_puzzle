# 8-Puzzle Solver

A Python application that solves the 8-puzzle problem using various AI search algorithms and a Kivy-based graphical user interface (GUI). The project implements Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening Search (IDS) and A* Search (with Manhattan and Euclidean heuristics) algorithms.

![Demo image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/demo_img.png)


## Features
- **Algorithms**: Solve the puzzle using BFS, DFS, IDS, or A* (Manhattan & Euclidean heuristics).
- **GUI**: Visualize the puzzle and step-by-step solution using a Kivy-based GUI.
- **Customizable Input**: Set initial puzzle configurations directly in the interface.

## Table of Contents
1. [About the Project](#about-the-project)
2. [Algorithms](#algorithms)
3. [Demo](#demo)
4. [Comparison](#comparison)

### About the Project
#### 🔍 Solving the classic 8-puzzle with AI search agents
This project implements a range of informed and uninformed search algorithms to tackle the 8-puzzle problem and bringing theoretical search methodologies to practical application in solving the 8-puzzle problem.

#### ✨ Interactive GUI
Engage with AI-driven puzzle-solving through an intuitive Kivy-based GUI. Shuffle the tiles, select an algorithm, and observe the solution unfold step-by-step.

#### 👥 Solve it Yourself
The application also allows users to attempt solving the puzzle independently, moving tiles manually to explore different solution paths and strategies.

### Algorithms
The application implements the following search algorithms:

#### 1 - Breadth-First Search (BFS)
##### Description
A searching algorithm that explores all possible moves level-by-level until the solution is found (explores the shallowest first). Always guarantees the optimal and shortest solution path.
##### Pseudocode
![image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/bfs.png)
##### Analysis
- Time Complexity: O(b<sup>d</sup>), Where b is the branching factor, and d is the depth of the solution.  <br>
- Space Complexity: O(b<sup>d</sup>) The algorithm must store all nodes at the current depth in the frontier, leading to high memory usage.<br>
- Completeness: <br>
  BFS is complete, it will always find a solution to a solvable puzzle.<br>
- Optimality:<br>
  BFS is optimal as it always finds the shortest path to the solution.

#### 2 - Depth-First Search (DFS)
##### Description
A searching algorithm that explores paths as deep as possible before backtracking.
##### Pseudocode
![image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/dfs.png)
##### Analysis
- Time Complexity: O(b<sup>m</sup>), Where b is the branching factor, and m is the maximum depth reached. <br>
- Space Complexity: O(b.m)
- Completeness: <br>
 It is complete for this specific problem as the 8-puzzle problem has a finite state space with a maximum of 9! (362,880) possible configurations. This finite nature ensures that DFS will eventually reach the goal if the puzzle is solvable, thus making it complete.
- Optimality:<br>
  DFS is not optimal for the 8-puzzle since it can find a solution that is not the shortest path.

#### 3 - Iterative Deepening Search (IDS)
##### Description
 IDS combines the space efficiency of Depth-First Search (DFS) with the completeness of Breadth-First Search (BFS). Since it systematically explores all depths and ensures that each level is fully explored before moving deeper.
##### Pseudocode
![image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/ids.png)
<br>
![image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/dls.png)
##### Analysis
- Time Complexity: O(b<sup>d</sup>), Where b is the branching factor, and d is the depth of the solution.  <br>
- Space Complexity: O(b.d), It requires memory proportional to the maximum depth being searched at any given time.<br>
- Completeness: <br>
  IDS is complete since it will eventually reach all nodes at depth 𝑑 and find a solution if the puzzle is solvable.<br>
- Optimality:<br>
  IDS is optimal as it will find the solution that is the closest to the initial state.

#### 4 - A* Search
##### Description
A heuristic-driven search that evaluates the puzzle state by estimating the cost to reach the solution:
- Manhattan Distance: Calculates the total moves required based on vertical/horizontal distance. <br>
- Euclidean Distance: Uses a straight-line distance metric between tiles and target positions.<br>
##### Pseudocode
![image](https://github.com/RanaMohamed6720/8_puzzle/blob/main/assets/a_star.png)
##### Analysis
- Time Complexity: O(b<sup>d</sup>), Where b is the branching factor, and d is the depth of the solution.  <br>
- Space Complexity: O(b<sup>d</sup>) A* stores all nodes in the frontier and explored sets, which can become very large.<br>
- Completeness: <br>
  A* is complete for the 8-puzzle problem because it explores all possible paths until it finds a solution.<br>
- Optimality:<br>
  A* is optimal as it will always find the least-cost solution.
### Demo
<div align="center">

[Demo](https://github.com/user-attachments/assets/958963b4-4049-4012-bbec-7c33c646db09)

</div>

### Comparison
<h2>Algorithm Comparison</h2>
<table>
    <thead>
        <tr>
            <th>Algorithm</th>
            <th>Time Complexity</th>
            <th>Space Complexity</th>
            <th>Completeness</th>
            <th>Optimality</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>BFS</td>
            <td>O(b<sup>d</sup>)</td>
            <td>O(b<sup>d</sup>)</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>DFS</td>
            <td>O(b<sup>m</sup>)</td>
            <td>O(b ⋅ m)</td>
            <td>No</td>
            <td>No</td>
        </tr>
        <tr>
            <td>DLS</td>
            <td>O(b<sup>limit</sup>)</td>
            <td>O(b ⋅ limit)</td>
            <td>Yes (if depth limit is sufficient)</td>
            <td>No</td>
        </tr>
        <tr>
            <td>IDS</td>
            <td>O(b<sup>d</sup>)</td>
            <td>O(b ⋅ d)</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>A*</td>
            <td>O(b<sup>d</sup>)</td>
            <td>O(b<sup>d</sup>)</td>
            <td>Yes</td>
            <td>Yes</td>
        </tr>
    </tbody>
</table>


### Requirements
- Python 3.x
- Kivy

### Install Dependencies
```bash
pip install kivy
```
