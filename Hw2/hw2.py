from search import *
from random import shuffle
import time

class EightPuzzle(Problem):
    def __init__(self, hardness='hard'):
        super().__init__(initial=self.generate_init(hardness), goal=tuple(list(range(9))))


    def actions(self, state):
        action_dict = {
            0: ['Right', 'Down'],
            1: ['Left', 'Right', 'Down'],
            2: ['Left', 'Down'],
            3: ['Up', 'Right', 'Down'],
            4: ['Up', 'Left', 'Right', 'Down'],
            5: ['Up', 'Left', 'Down'],
            6: ['Up', 'Right'],
            7: ['Left', 'Up', 'Right'],
            8: ['Left', 'Up']
        }
        for ind, el in enumerate(state):
            if el == 0:
                #print(action_dict[ind])
                return action_dict[ind]

    def result(self, state, action):
        empty_cell_ind = None
        for ind, el in enumerate(state):
            if el == 0:
                empty_cell_ind = ind
                break
        if empty_cell_ind == None:
            assert False, 'empty cell not found in state'

        successor = [el for el in state]
        if action == 'Up':
            successor[empty_cell_ind] = state[empty_cell_ind-3]
            successor[empty_cell_ind-3] = 0
        elif action == 'Down':
            successor[empty_cell_ind] = state[empty_cell_ind+3]
            successor[empty_cell_ind+3] = 0
        elif action == 'Left':
            successor[empty_cell_ind] = state[empty_cell_ind-1]
            successor[empty_cell_ind-1] = 0
        elif action == 'Right':
            successor[empty_cell_ind] = state[empty_cell_ind+1]
            successor[empty_cell_ind+1] = 0
        else:
            assert False, 'undefined action'
        #print(successor)
        return tuple(successor)
    def goal_test(self, state):
        for ind, el in enumerate(state):
            if ind != el:
                return False
        return True

    def generate_init(self, hardness):
        print("starting...")
        if hardness == 'easy':
            return tuple([1, 2, 0, 3, 4, 5, 6, 7, 8])
        else:
            def random_puzzle():
                puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                random.shuffle(puzzle)
                puzzle = tuple(puzzle)
                return puzzle

            def is_solvable(puzzle):
                inversions = 0
                for i in range(9):
                    for j in range(i+1, 9):
                        if puzzle[j] and puzzle[i] and puzzle[i] > puzzle[j]:
                            inversions += 1
                #print(inversions)
                if inversions % 2 == 0:
                    #print("its solvable")
                    return True
                else:
                    return False
            while True:
                rp = random_puzzle()
                if is_solvable(rp):
                    return rp
                else:
                    continue

    def print_state(self, state):
        for i in range(3):
            print(state[i*3:(i+1)*3])
        print()

    def h(self, node):
        coord_map = {
            0: (0, 0),
            1: (0, 1),
            2: (0, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (2, 0),
            7: (2, 1),
            8: (2, 2)
        }
        hh = 0
        for ind, el in enumerate(node.state):
            curr_coord = coord_map[ind]
            dest_coord = coord_map[el]
            hh += abs(curr_coord[0] - dest_coord[0]) + abs(curr_coord[1] - dest_coord[1])
        #print(hh)
        return hh

print("\n--- 8 PUZZLE ---\n")

print("A* SEARCH")
print("-----------")
a_front = 0
a_expl = 0
start_time_astar = time.time()
for i in range(5):
    eight_puzzle_astar = EightPuzzle()
    _, f, e = astar_search(eight_puzzle_astar)
    a_front += f
    a_expl += e
print("\nAverage A* search time: %s seconds" % ((time.time() - start_time_astar)/5))
print("Average A* storage: ", a_front/5)
print("Average A* explored:", a_expl/5)

print("\n\nRBFS")
print("------")
r_front = 0
r_expl = 0
start_time_rbfs = time.time()
for i in range(5):
    eight_puzzle_rbfs = EightPuzzle()
    _, fr, ex = recursive_best_first_search(eight_puzzle_rbfs)
    r_front += fr
    r_expl += ex
print("\nAverage RBFS search time: %s seconds" % ((time.time() - start_time_rbfs)/5))
print("Average RBFS storage: ", r_front/5)
print("Average RBFS explored:", r_expl/5)
