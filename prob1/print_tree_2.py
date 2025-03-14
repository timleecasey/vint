

from enum import Enum


debug = False

class Mode(Enum) :
    NONE = 0
    #
    # Mode for moving a node up
    #
    UP = 1
    #
    # Mode for rotating a node through part of the tree
    #
    ROTATE = 2
    #
    # Mode for rotating a child into a new branch.
    ROTATE_NEW_CH = 3



class Node:
    def __init__(self, val, m=1) :
        self.val = val
        self.parent = None
        self.children = [None] * m


    def remove_node(self, n) -> None :
        to_remove = -1
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                if self.children[i].val == n.val :
                    to_remove = i
                    break

        if debug : print(f"removed {n.val} from par {self.val} at pos {i}")
        if to_remove != -1 :
            self.children[to_remove] = None
        
        n.parent = None

    def add_node(self, n) -> None :
        prev = None
        for i in range(len(self.children)) :
            if self.children[i] is None :
                n.parent = self
                self.children[i] = n
                if debug : print(f"placed {n.val} in par {self.val} at pos {i}")
                if prev is not None :
                    prev.right = n
                break
            prev = self.children[i]

    def tostring(self) -> str :
        return str(self.val)


    def is_leaf(self) -> bool :
        ch_count = self.empty_link_count()
        return ch_count == len(self.children)

    def is_full(self) -> bool :
        ch_count = self.empty_link_count()
        return ch_count == 0
        
    def first_child(self) -> 'Node' :
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                return self.children[i]
        return None

    def last_child(self) -> 'Node' :
        n = None
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                n = self.children[i]
        return n
        

    def empty_link_count(self) -> int :
        count = 0
        for i in range(len(self.children)) :
            if self.children[i] is None :
                count += 1
        return count
        
    def print(self, pad) :
        empty = ""
        for i in range(len(self.children)) :
            if self.children[i] is None :
                empty = empty + "."

        if self.parent is None :
            p_val = "root"
        else :
            p_val = str(self.parent.val)
        print(f"{pad}{p_val}->{self.val}{empty}")
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                self.children[i].print(pad)
                #pad = pad + "  "

    def least(self) -> 'Node' :
        least_node = self
        found = False
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                if self.children[i].val < least_node.val :
                    least_node = self.children[i]
                    found = True
        if found : 
            least_node = least_node.least()

        return least_node

    def greatest(self) -> 'Node' :
        greatest_node = self
        found = False
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                if self.children[i].val > greatest_node.val :
                    greatest_node = self.children[i]
                    found = True
        if found : 
            greatest_node = greatest_node.greatest()

        return greatest_node

    def rightmost(self) -> 'Node' :
        right = None
        for i in range(1, len(self.children)) :
            if self.children[i] is not None :
                right = self.children[i]
        return right

    def leftmost(self) -> 'Node' :
        return self.children[0]


    def left_leaf(self) -> 'Node' :
        if self.is_leaf() :
            return self
        left = self.leftmost()
        return left.left_leaf()
 
    def right_leaf(self) -> 'Node' :
        if self.is_leaf() :
            return self
        right = self.rightmost()
        if right is None :
            return None
        return right.left_leaf()


    def size(self, seed=0) -> int :
        count = seed + 1
        for i in range(len(self.children)) : 
            if self.children[i] is not None :
                count = self.children[i].size(count)
        return count


    #
    # The number of subnodes in each of the children
    #
    def children_sizes(self) -> [] :
        num_children = len(self.children)
        counts = [0] * num_children
        for i in range(num_children) : 
            if self.children[i] is not None :
                counts[i] = self.children[i].size()
            else :
                counts[i] = 0
        return counts
        

class Tree:
    def __init__(self, n=1, m=1) :
        self.count = 0
        self.m = m
        self.n = n
        self.root = None


    def remove_from(self, parent, n) -> None :
        parent.remove_node(n)


    def add_to(self, parent, n) -> None :
        if parent is not None :
            parent.add_node(n)


    def add_node(self, parent, val) -> Node :
        if self.root is None :
            n = Node(val, self.m)
            self.root = n
            return n

        if parent is None :
            print("Could not add, empty parent")
            return None

        n = Node(val, self.m)
        parent.add_node(n)
        return n


    def print(self) :
        self.count += 1
        print(f"#:{self.count} N:{self.n} M:{self.m}")
        if self.root is not None :
            self.root.print("")
        else :
            print("empty")


    def root(self) -> Node :
        return t.root


def build_left_linear_tree(n, m) -> Tree :
    t = Tree(n, m )
    t.add_node(None, n-1)
    t.parent = t.root
    parent = t.root
    val = n - 2
    rank = 1
    node = None
    for i in range(n - 1, 0, -1) :
        if node is not None :
            t.parent = node
        node = t.add_node(parent, val)
        val -= 1
        t.rank = rank
        rank += 1
        parent = node

    if t.n < t.m + 1 :
        return t

    return t


def find_next_node(t, trav) -> Mode :

    tv = "--"
    if trav is not None :
        tv = str(trav.val)
    if debug : print(f"FIND_NEXT  {tv}")

    size = -1 
    diff = -1
    mode = Mode.NONE

    #
    # To know to move a node, look at the children sizes
    #
    children_sizes = trav.children_sizes()
    size = 0
    max = 0
    min = t.n
    max_index = -1
    min_index = -1
    for i in range(len(children_sizes)) :
        size += children_sizes[i]
        if children_sizes[i] < min :
            min = children_sizes[i]
            min_index = i
        if children_sizes[i] > max :
            max = children_sizes[i]
            max_index = i

    diff = max - min

    if debug : print(f"CAN MOVE check diff {diff} max {max} @ {max_index} min {min} @ {min_index}")
    if diff == 0 :
        if debug : print("LEVEL")
        mode = Mode.UP
    else :
        #
        # Skip max, and up to the index
        #
        for i in range(max_index + 1, min_index + 1) :
            if debug : print(f"FIND_NEXT max {children_sizes[max_index]} size {children_sizes[i]} @ {i} for total {size}")
            if children_sizes[max_index] - children_sizes[i] > 1 :
                if children_sizes[i] == 0 or max - children_sizes[i] < 2 :
                    mode = Mode.ROTATE_NEW_CH
                else :
                    mode = Mode.ROTATE
                break
            else :
                mode = Mode.UP

    if debug : print(f"NEXT mode {mode} size {size} diff {diff} M {t.m}")
    return mode
    return t

def unwind_right(t, node) :
    if debug : print(f"UNWIND {node.val}")

    right_ch = node.rightmost()

    while right_ch is not None :
        t.remove_from(node, right_ch)
        left_leaf = node.left_leaf()

        t.add_to(left_leaf, right_ch)
        right_ch = node.rightmost()

    if debug : print("UNWIND DONE")


def move_nodes(t, mode, trav) :

    if debug : print(f"MOVE {mode} {trav.val}")

    if mode == Mode.ROTATE :

        left_leaf = trav.left_leaf()
        prev_par = left_leaf.parent
        t.remove_from(prev_par, left_leaf)

        right_leaf = trav.right_leaf()
        t.add_to(right_leaf, left_leaf)

    elif mode == Mode.ROTATE_NEW_CH :

        left_leaf = trav.left_leaf()
        prev_par = left_leaf.parent

        t.remove_from(prev_par, left_leaf)

        t.add_to(trav, left_leaf)

    elif mode == Mode.UP :

        unwind_right(t, trav)

        parent = trav.parent

        left_leaf = trav.left_leaf()
        prev_par = left_leaf.parent

        t.remove_from(prev_par, left_leaf)
        t.add_to(parent, left_leaf)

    else :
        print("Unknown mode")

    if debug : print(f"MOVE done")


def permute_at(t, n) :
    if n is None :
        return
    if n.is_leaf() :
        return
    if n.size() < 3 :
        return

    if not n.is_leaf() :
        for i in range(len(n.children)) :
            permute_at(t, n.children[i])
    
    while True :
        mode = find_next_node(t, n)
        if mode is Mode.UP or mode is Mode.NONE :
            break
        if mode is None :
            break
        move_nodes(t, mode, n)
        t.print()
        if t.count > 100 :
            print(f"STOPPING for overage {t.count}")
            break

    unwind_right(t, n)
    if debug : print(f"PERMUTE DONE @ {n.val}")

    

def permute_tree(t) -> Tree :
    t.print()
    permute_at(t, t.root)

t = build_left_linear_tree(5, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (7)")


t = build_left_linear_tree(7, 2)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (10)")

t = build_left_linear_tree(4, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (4)")
