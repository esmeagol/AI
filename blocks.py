import random
import sys
from copy import deepcopy
from heapq import heappush, heappop

#goal = [[],[],[8,7,6,5,4,3,2,1]]
goal = [[],[],[8,7,6,5,4,3,2,1]]

def find(f, seq):
  """Return first item to be found in the list matching with 'item'."""
  for item in seq:
    if f == item: 
      return item

  return None

def print_blocks(stack_list):
    max_blocks = 0
    for i in range(len(stack_list)):
        max_blocks = max(max_blocks, len(stack_list[i]))

    array = []
    for i in range(max_blocks):
        temp_list = []
        for j in range(len(stack_list)):
            k = max_blocks - i - 1
            if k < 0 or k >=len(stack_list[j]):
                temp_list.append(' ')
            else:
                temp_list.append(stack_list[j][k])

        array.append(temp_list)

    for i in range(max_blocks):
        print(' '.join(map(str, array[i])))
    print('\n')
    print('\n')

def gen_children(stack_list):
    list_of_children = []
    sl = stack_list
    for i in range(len(sl)):
        cur_stack = sl[i]
        len_cur = len(cur_stack)
        if not len_cur:
            continue

        for j in range(len_cur):
            for k in range(len(sl)):
                if k != i:
                    new_child = deepcopy(sl)
                    count = 0
                    for l in cur_stack[len_cur-j-1:]:
                        new_child[k].append(l)
                        count +=1
                    for p in range(count):
                        new_child[i].pop()
                    list_of_children.append(new_child)

    return list_of_children

def calc_heuristics(sl):
    h_cost = 14
    for i in range(len(sl)):
        cur_stack = sl[i]
        temp = 0
        for j in cur_stack:
            if temp:
                if j == temp-1:
                    #print('decreasing cost', j, 'follows', temp)
                    h_cost -= 4
                else:
                    if j < temp:
                        #print('increasing cost', j, 'follows', temp)
                        h_cost -= 2
                    else:
                        h_cost += 2
            temp = j

    return h_cost


class BlocksWorld(object):

    def __init__(self, num_blocks=8):
        self.stack_list = [[1,2,3,4,5,6,7,8],[],[]]
        #self.stack_list = [[],[],[8,7,6,5,4,3,2,1]]
        self.heap = []



    def uniform_cost(self):
        h = []
        seen = []
        g_cost = 0
        new_node = self.stack_list
        h_cost = calc_heuristics(new_node)
        cost = g_cost + h_cost
        heappush(h, (cost, g_cost, new_node))

        while len(h):
            (cost, g_cost, new_node) = heappop(h)
            seen.append(new_node)
            print('cost = ', cost, 'g = ', g_cost)
            print_blocks(new_node)

            if cost > 150:
                print('cost exceeded limit')
                break

            if new_node == goal:
                print('goal found. cost =', cost, 'g =', g_cost)
                break

            child_list = gen_children(new_node)
            g_cost+= 1
            for node in child_list:
                if new_node == goal:
                    print('goal found. cost =',cost,'g =',g_cost)
                    print_blocks(new_node)
                    break

                if not find(node, seen):
                    h_cost = calc_heuristics(node)
                    cost = g_cost + h_cost
                    heappush(h, (cost, g_cost, node))


def main():
    if len(sys.argv) != 2:
        print('usage: %s <num_blocks>' % sys.argv[0])
    
    a = BlocksWorld()

    print(a.stack_list)
    print_blocks(a.stack_list)
    a.uniform_cost()

    return

if __name__ == '__main__':
    main()
