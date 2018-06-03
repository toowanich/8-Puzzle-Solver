# 8-Puzzle-Solver
## About
Program to find the solution to a given 8 Puzzle State. This program was created as an assigned projected for the CSS333 Parallel and Distributed Computing Class.

### Requirements
1. Python 3 (https://www.python.org/downloads/)
2. AnyTree (http://anytree.readthedocs.io/)

## Installation

### Python 3
1.  Download the latest version of Python 3 from [here](https://www.python.org/downloads/).
- Follow the installation instructions provided.
  - The installation should also include the pip installer.
  - If it is not installed by default you can follow the instructions [here](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line) to install it.

### AnyTree
1. Open a command prompt / terminal window
  - Run ``pip install anytree``
  - If you are using a Windows machine you may need to navigate to your python installation and run ```python -m pip install anytree``` instead.

### 8 Puzzle Solver
1. Download the from the repository as a zip file.
- Extract to desired directory.

## Running Instructions
1. Start (Double click) main.py file.
2. Follow the instructions shown in the command line

## Algorithm
We used a greedy best first search approach to solve this problem. Since we generate the tree sequentially, we do not have complete information of the problem space for each input. The algorithm picks the node with the lowest weight (best first) of the leaf nodes without regard for their depth. The algorithm contains parallel processing in two areas, the generation of states and the calculation of each state’s weight. Due to the problem’s nature, we can only divide the workload between a maximum of 4 processes at any given time, since each state can have a maximum of 4 children. 

### Members:
- 5822780276 Puttiwat Wanna
- 5822784179 Pawat Treepoca
- 5822800025 Wanich Keatkajonjumroen
