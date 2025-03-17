

from enum import Enum


debug = True

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
        for i in range(len(self.children)) :
            if self.children[i] is None :
                n.parent = self
                self.children[i] = n
                if debug : print(f"placed {n.val} in par {self.val} at pos {i}")
                break

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

        ch_tag = "["
        for i in range(len(self.children)) :
            if self.children[i] is None :
                ch_tag = ch_tag + "."
            else :
                ch_tag = ch_tag + "|"
        ch_tag = ch_tag + "]"

        if self.parent is None :
            p_val = "root"
        else :
            p_val = str(self.parent.val)
        print(f"{pad}{p_val}->{self.val}:{ch_tag}")
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


    def rightmost_left_leaf(self, left_of) -> 'Node' :
        if self.is_leaf() :
            print(f"RMLL picked {self.val}")
            return self
        right = None
        len_of_ch = len(self.children)
        for i in range(left_of - 1, -1, -1) :
            if self.children[i] is not None and self.children[i].size() > 1 :
                if debug : print(f"RMLL picking {self.val} {i}")
                right = self.children[i].rightmost_left_leaf(len_of_ch)
                break

        rval = "--"
        if right is not None :
            rval = str(right.val)
        print(f"RMLL picked {rval}")
        if right is None :
            right = self.left_leaf()
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


    def children_sizes(self) :
        count = 0
        sizes = [] * len(self.children)
        for i in range(len(self.children)) : 
            if self.children[i] is not None :
                sizes[i] = self.children[i].size()
            else :
                sizes[i] = 0
        return sizes
        


    def find_leaf(self) -> int :
        if self.is_leaf() :
            return self

        for i in range(len(self.children)) :
            if self.children[i] is not None :
                return self.children[i].find_leaf()
        return None

    def total_leaves(self) -> int :
        if self.is_leaf() :
            return 1

        count = 0
        for i in range(len(self.children)) :
            if self.children[i] is not None :
                count += self.children[i].total_leaves()
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


    def gather_children(self) -> ['Node'] :
        child_container = []
        for i in range(len(self.children)) : 
            if self.children[i] is not None :
                child_container.append(self.children[i])

        return child_container
        

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


class LevelContext :
    def __init__(self) :
        self.left_fill = 0
        self.right_fill = 1
        self.mode = Mode.ROTATE_NEW_CH
        self.trav = None
        self.rotate_from = -1
        self.rotate_to = -1
        # Used for validation if debugging
        self.labels = {}

    def can_continue(self) -> bool :
        if self.mode is Mode.UP :
            return False
        if self.mode is Mode.NONE :
            return False
        return True

# Add to new child from child pool with in the sub tree and reset all nodes to linear left tree
# rotate nodes in new rank until full, at or close to level
# if any child has more than 1 node and there is a free slot, repeat

def find_next_node(t, ctx) -> Mode :

    trav = ctx.trav

    tv = "--"
    if trav is not None :
        tv = str(trav.val)
    if debug : print(f"FIND_NEXT  {tv}")


    size = -1 
    diff = -1
    sizes = trav.children_sizes()

    if ctx.mode is Mode.ROTATE_NEW_CH :
        ctx.mode = Mode.ROTATE
        ctx.rotate_from = 0
        ctx.rotate_to = 1

    left = ctx.left_fill
    right = ctx.right_fill

    size = 0

    max = 0
    max_index = -1

    min = t.n
    min_index = -1

    for i in range(left, right) :
        size += sizes[i]
        if sizes[i] < min :
            min = sizes[i]
            min_index = i
        #
        # The last max, not the first max
        #
        if sizes[i] >= max :
            max = sizes[i]
            max_index = i


    if size < 3 :
        ctx.mode = Mode.UP
        
    if debug :
        size_str = ".".join([str(i) for i in sizes])
        print(f"ROTATE rotation {trav.val} from {ctx.left_fill} to {ctx.right_fill} with sizes {size_str}")

    while sizes[ctx.rotate_from] - sizes[ctx.rotate_to] <= 1 :
        ctx.rotate_to += 1
        if ctx.rotate_to >= ctx.right_fill :
            break

    if ctx.rotate_to < ctx.right_fill :
        if debug : print(f"ROTATE node {trav.val} from {ctx.rotate_from} size {sizes[ctx.rotate_from]} to {ctx.rotate_to} size {sizes[ctx.rotate_to]}")
        return ctx.mode
    else :
        ctx.rotate_from = -1
        ctx.rotate_to = -1


    ctx.mode = Mode.ROTATE_NEW_CH
    if right == t.m or right >= size:
        ctx.mode = Mode.NONE

    if debug : print(f"NEXT mode {ctx.mode} left {left} right {right} size {size} M {t.m}")

    return ctx.mode


def unwind_at_node(t, node) :
    if debug : print(f"UNWIND {node.val}")

    right_ch = node.rightmost()

    while right_ch is not None :
        t.remove_from(node, right_ch)
        left_leaf = node.left_leaf()

        t.add_to(left_leaf, right_ch)
        right_ch = node.rightmost()

    if debug : print("UNWIND DONE")


def move_nodes(t, ctx) :

    trav = ctx.trav
    mode = ctx.mode

    if debug : print(f"MOVE {mode} {trav.val}")

    if mode == Mode.ROTATE :


        if debug : print(f"ROTATE node {trav.val} from {ctx.rotate_from} to {ctx.rotate_to}")

        left_leaf = trav.children[ctx.rotate_from].rightmost_left_leaf(ctx.right_fill)
        prev_par = left_leaf.parent
        t.remove_from(prev_par, left_leaf)

        if trav.children[ctx.rotate_to] is None :
            right_leaf = trav
        else :
            right_leaf = trav.children[ctx.rotate_to].find_leaf()

        rlval = "--"
        if right_leaf is not None :
            rlval = str(right_leaf.val)
        if debug : print(f"ROTATE picked {rlval} for {left_leaf.val}")

        t.add_to(right_leaf, left_leaf)

    elif mode == Mode.ROTATE_NEW_CH :


        par = None
        leaf = None

        if ctx.right_fill > 1 :
            for i in range(ctx.right_fill - 1, ctx.left_fill - 1, -1) :
                if trav.children[i].size() > 1 :
                    leaf = trav.children[i].find_leaf()
        else :
            leaf = trav.left_leaf()

        if leaf is not None  :
            par = leaf.parent
            t.remove_from(par, leaf)

            t.add_to(trav, leaf)
            ctx.right_fill += 1


            if debug : print(f"Rebalancing")

            #
            # Restart filling and balancing
            #
            ch_len = len(trav.children)
            left_leaf = trav.left_leaf()

            #
            # Skip the far left
            #
            for i in range(ch_len - 1, 0, -1) :
                if trav.children[i] is not None :
                    fill = trav.children[i].gather_children()
                    if debug : print(f"Rebalancing child {trav.children[i].val} found {len(fill)}")
                    for j in range(len(fill)) :
                        t.remove_from(fill[j].parent, fill[j])
                    for j in range(len(fill)) :
                        t.add_to(left_leaf, fill[j])
                        left_leaf = fill[j].find_leaf()

    elif mode == Mode.UP :

        unwind_at_node(t, trav)

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

    
    ctx = LevelContext()
    ctx.trav = n
    ctx.mode = Mode.ROTATE_NEW_CH
    ctx.left_fill = 0
    ctx.right_fill = 1
    ctx.rotate_from = -1
    ctx.rotate_to = -1
    ctx.labels = {}

    while ctx.can_continue() :
        move_nodes(t, ctx)
        t.print()
        if debug :
            # 
            # check for in-correct number of children
            #
            if ctx.trav.total_leaves() > t.m :
                raise ValueError(f"Total leaves exceeded {ctx.trav.val}")

            #
            # Check for a previously seen configuration within this layer of the tree
            #
            sizes = ctx.trav.children_sizes()
            sizes = sorted(sizes)
            label = ".".join([str(i) for i in sizes])
            print(f"LABEL @ {t.count} : {label}")
            if label in ctx.labels :
                raise ValueError(f"Seen before {label} for {ctx.trav.val}")
            ctx.labels[label] = 1
        
        find_next_node(t, ctx)
        if t.count > 10000 :
            print(f"STOPPING for overage {t.count}")
            break

    unwind_at_node(t, n)
    if debug : print(f"PERMUTE DONE @ {n.val}")

    

def permute_tree(t) -> Tree :
    t.print()
    permute_at(t, t.root)


if True :
    for i in range(5, 100) :
        for j in range(4, 10) :
            t = build_left_linear_tree(i, j)
            permute_tree(t)
            print(f"DONE COUNT: N:{i},M:{j} {t.count}")

t = build_left_linear_tree(7, 2)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (10)")

t = build_left_linear_tree(4, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (4)")

t = build_left_linear_tree(5, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (7)")

t = build_left_linear_tree(6, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (11)")

t = build_left_linear_tree(7, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (17)")

t = build_left_linear_tree(8, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (23)")

t = build_left_linear_tree(30, 3)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (491)")

t = build_left_linear_tree(6, 4)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (13)")

t = build_left_linear_tree(7, 4)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (21)")

t = build_left_linear_tree(8, 4)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (31)")

t = build_left_linear_tree(9, 4)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (43)")

t = build_left_linear_tree(7, 5)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (23)")

t = build_left_linear_tree(8, 5)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (35)")

t = build_left_linear_tree(8, 6)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (37)")

t = build_left_linear_tree(9, 7)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (56)")

t = build_left_linear_tree(10, 8)
permute_tree(t)
print(f"DONE COUNT: N:{t.n},M:{t.m} {t.count} (81)")


