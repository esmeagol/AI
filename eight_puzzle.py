import random
import sys
from collections import deque

# goal node
goal = [1,2,3,  \
        4,0,5,  \
        6,7,8]

#list defining valid moves for each position in eight puzzle
valid_moves = [[1,3],[0,2,4],[1,5], \
                [0,4,6],[1,3,5,7],[2,4,8], \
                [3,7],[4,6,8],[5,7]]

#globals to represent output values
solution_depth = 0
num_goal_tests = 0
max_queue_size = 0


MAX_NUM_ITERATIONS = 500000

# maximum value of depth for iterative deepening algorithm
MAX_ID_DEPTH = 20

def find(f, seq):
  """Return first item to be found in the list matching with 'item'."""
  for item in seq:
    if is_equal(f, item): 
      return item

  return None

def is_equal(a, b):
    """ compares two boards, returns true if equal """
    for i in range(9):
        if a[i] is not b[i]:
            return False
    return True

class eight_board(object):

    def __init__(self, board=[1,2,3,4,0,5,6,7,8]):
        self.board = board

    def print_board(self):
        print(' '.join(map(str, self.board[0:3])))
        print(' '.join(map(str, self.board[3:6])))
        print(' '.join(map(str, self.board[6:9])))
        print('\n')


    def multi_shuffles(self, moves = 30):
        for i in range(moves):
            zero_pos = self.board.index(0)
            m = random.choice(valid_moves[zero_pos])
            temp = self.board[zero_pos]
            self.board[zero_pos] = self.board[m]
            self.board[m] = temp

    def is_goal(self):
        return is_equal(self.board, goal)

    def dfs(self, max_depth = 20):
        num_goal_tests = 0
        max_queue_size = 0
        result = False

        stack = [[self.board, 0]]
        max_queue_size = len(stack)
        seen = []
        while True:
            if not len(stack):
                break
            current = stack.pop()
            self.board = current[0]
            #self.print_board()
            seen.append(current[0])
            num_goal_tests += 1

            if self.is_goal():
                self.print_board()
                solution_depth = current[1]
                result = True
                break
            
            if num_goal_tests > MAX_NUM_ITERATIONS:
                result = False
                break

            if current[1] > max_depth:
                continue

            children = self.create_children()
            child_depth = current[1] + 1
            for child in children:
                if not find(child, seen):
                    stack.append([child, child_depth])
                    max_queue_size = max(max_queue_size, len(stack))

        if result:
            print('solution depth: ' + str(solution_depth))
            print('num_goal_tests: ' + str(num_goal_tests))
            print('max queue size: ' + str(max_queue_size))
        return result
            

    def bfs(self):
        solution_depth = 0
        num_goal_tests = 0
        max_queue_size = 0
        result = False

        this_level = 1
        level = 0
        next_level = 0
        queue = deque([self.board])
        max_queue_size = len(queue)
        seen = []
        print('solution path:')
        while True:
            if not len(queue):
                result = False
                break

            current = queue.popleft()
            this_level -= 1
            self.board = current
            #self.print_board()
            seen.append(current)
            num_goal_tests += 1
            if self.is_goal():
                self.print_board()
                result = True
                break

            if num_goal_tests > MAX_NUM_ITERATIONS:
                result = False
                break

            children = self.create_children()
            solution_depth += 1
            for child in children:
                if not find(child, seen):
                    #self.print_board()
                    queue.append(child)
                    #print('adding child ', child)
                    
                    next_level += 1
                    max_queue_size = max(max_queue_size, len(queue))

            if this_level == 0:
                level += 1
                this_level = next_level
                next_level = 0

        if result:
            print('solution depth: ' + str(level))
            print('num_goal_tests: ' + str(num_goal_tests))
            print('max queue size: ' + str(max_queue_size))

        return result

    def itr_deep(self, depth = MAX_ID_DEPTH):
        for i in range(depth):
            if self.dfs(i):
                return True

        return False

    def create_children(self):
        children = []

        zero_pos = self.board.index(0)
        for m in valid_moves[zero_pos]:
            new_board = list(self.board)
            new_board[zero_pos] = self.board[m]
            new_board[m] = self.board[zero_pos]

            children.append(new_board)

        return children


def main():
    a = eight_board()
    print('goal: \n')
    a.print_board()


    if not sys.argv[2]:
        print('usage: %s <search_type> <num_scramble_steps>' % sys.argv[0])
        return

    a.multi_shuffles(int(sys.argv[2]))
    print('random initial state after ' + str(sys.argv[2]) + ' shuffles: \n')
    a.print_board()

    if not sys.argv[1]:
        print('usage: %s <search_type> <num_scramble_steps>' % sys.argv[0])
        return

    print(sys.argv[1] + '\n')
    if sys.argv[1] == 'bfs':
        a.bfs()
    if sys.argv[1] == 'dfs':
        a.dfs()
    if sys.argv[1] == 'id':
        a.itr_deep()

    return

if __name__ == '__main__':
    main()
