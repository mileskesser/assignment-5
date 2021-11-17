# Name: Miles Kesser
# OSU Email: kesserm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5 AVL Tree Implementation
# Due Date: 16 November 2021
# Description: AVL tree implementation
import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty
    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with ##print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty
    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with ##print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None
        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.
        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False
                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True

    # ----------------------------------------------------------------------
    def get_left_height(self, node):
        """
        Returns height left of a node
        """
        # Height of nodes left child
        return self.height(node.left)

    def get_right_height(self, node):
        """
        Returns height right of a node
        """
        # Height of nodes right child
        return self.height(node.right)

    def height(self, n):
        """
        Returns height of given node
        """
        # If node is None
        if n is None:
            return -1
        # If both nodes children are None
        if n.left is None and n.right is None:
            return 0
        # Recursive calculation to get height
        return 1 + max(self.height(n.left), self.height(n.right))

    def update_height(self, node):
        """
        Updates the height of a node
        """
        # Set new height
        node.height = self.height(node)

    def rotate_left(self, n):
        """
        Rotates left about a node
        """
        # Sets left child to C
        c = n.right
        # Nodes child becomes Cs left child
        n.right = c.left
        # If Cs left child exists
        if n.right is not None:
            # Cs left child becomes nodes right child
            n.right.parent = n
        # Cs left child in node
        c.left = n
        # Nodes parent becomes C
        n.parent = c
        # Update n and c heights
        self.update_height(n)
        self.update_height(c)

        return c

    def rotate_right(self, n):
        """
        Rotates right about a node
        """
        # Sets left child to C
        c = n.left
        # Nodes child becomes Cs right child
        n.left = c.right
        # If Cs right child exists
        if n.left is not None:
            # Cs right child becomes nodes left child
            n.left.parent = n
        # Cs right child becomes node
        c.right = n
        # Nodes parent is C
        n.parent = c
        # Update n and c heights
        self.update_height(n)
        self.update_height(c)

        return c

    def balance_factor(self, n):
        """
        Returns balance factor of a node
        """
        # Right height minus left height
        return self.get_right_height(n) - self.get_left_height(n)

    def rebalance(self, n):
        """
        Performs rebalancing at each node
        """
        # If root is LEFT heavy
        # Single rotation (minimum) needed
        if self.balance_factor(n) < -1:
            # Find if n parent is right or left heavy
            if n.parent is not None:
                if n.parent.right == n:
                    temp = "right"
                if n.parent.left == n:
                    temp = "left"
            # If child is RIGHT heavy
            # Double rotation needed
            if self.balance_factor(n.left) > 0:
                # Rotate subroot left
                n.left = self.rotate_left(n.left)
                # Update parent
                n.left.parent = n
            # Set temp parent to parent of n pre-rotation
            temp_parent = n.parent
            # Rotate right about n
            new_subtree_root = self.rotate_right(n)
            # Set new subtree root parent to old parent of n
            new_subtree_root.parent = temp_parent
            # Set n parent to the new subtree root
            n.parent = new_subtree_root
            # Set right of new subtree root to n
            new_subtree_root.right = n
            # Set ns old parents right or left to new subtree root
            if temp_parent is not None:
                if temp == "right":
                    temp_parent.right = new_subtree_root
                elif temp == "left":
                    temp_parent.left = new_subtree_root
            if temp_parent is None:
                self.root = new_subtree_root

        # If root is RIGHT heavy
        # Single rotation (minimum) needed
        elif self.balance_factor(n) > 1:
            # Find if n parent is right or left heavy
            if n.parent is not None:
                if n.parent.right == n:
                    temp = "right"
                if n.parent.left == n:
                    temp = "left"
            # If subroot is LEFT heavy
            # Double rotation needed
            elif self.balance_factor(n.right) < 0:
                # Rotate subroot right
                n.right = self.rotate_right(n.right)
                # Update parent
                n.right.parent = n
            # Set temp parent to parent of n pre-rotation
            temp_parent = n.parent
            # Rotate left about n
            new_subtree_root = self.rotate_left(n)
            # Set new subtree root parent to old parent of n
            new_subtree_root.parent = temp_parent
            # Set n parent to the new subtree root
            n.parent = new_subtree_root
            # Set left of new subtree root to n
            new_subtree_root.left = n
            # Set ns old parents right or left to new subtree root
            if temp_parent is not None:
                if temp == "right":
                    temp_parent.right = new_subtree_root
                elif temp == "left":
                    temp_parent.left = new_subtree_root
            if temp_parent is None:
                self.root = new_subtree_root
        else:
            # Update height
            self.update_height(n)

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree while maintaining its AVL property
        """
        # Create new node
        new_node = TreeNode(value)
        # Set cur to the root and node to None
        cur_node = self.root
        node = None
        # If tree is empty set as root
        if self.root is None:
            self.root = new_node

        # Set Node to Cur to follow its traversal
        else:
            while cur_node is not None:
                node = cur_node

                # Traverse the tree checking < or > for new location
                if new_node.value < cur_node.value:
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right

                    # Do not add if node value exists in tree
            if new_node.value == node.value:
                cur_node = self.root
                return
                # If new nodes value is less than
            elif new_node.value < node.value:
                # Set new node
                node.left = new_node
                # Set new nodes parent
                node.left.parent = node
                # Update heights
                self.update_height(node)
                self.update_height(node.left)

                n = new_node
                p = n.parent
                # Traverse up checking each parent until None
                while p is not None:
                    # Set a chaser
                    q = p
                    # Update height
                    self.update_height(p)
                    # Rebalance at parent
                    self.rebalance(p)
                    # Move up to next parent
                    p = p.parent
                    # Update height of root
                    self.update_height(self.root)
                # Set root to chaser
                self.root = q

            # If new nodes value is greater than
            else:
                node.right = new_node
                # Set new nodes parent
                node.right.parent = node
                # Update heights
                self.update_height(node)
                self.update_height(node.right)

                n = node.right
                p = n.parent
                # Traverse up checking each parent until None
                while p is not None:
                    # Set a chaser
                    q = p
                    # Update height
                    self.update_height(p)
                    # Rebalance at parent
                    self.rebalance(p)
                    # Move up to next parent
                    p = p.parent
                    # Update height of root
                    self.update_height(self.root)
                # Set root to chaser
                self.root = q

    def remove(self, value: object) -> bool:
        """
        Removes the value from the AVL tree. Return True if removed otherwise return False
        """
        # Create node with value to remove
        node_to_remove = TreeNode(value)
        # Set cur to the root and node to None
        cur_node = self.root
        node = None
        # If tree is one node
        if node_to_remove.value == self.root.value and self.root.left is None and self.root.right is None:
            self.root = None
            return True
        # If either value to remove or root is None
        if node_to_remove is None and cur_node is None:
            return False
        else:
            # Set Node to Cur to follow its traversal
            while cur_node.value != node_to_remove.value:

                # Traverse the tree checking < or > for node to remove
                if node_to_remove.value < cur_node.value:
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right
                    # Set node to remove, its parent, and its children
        n = cur_node
        p = n.parent
        right = n.right
        left = n.left

        # If removing leaf node
        if n.left is None and n.right is None:
            # If smaller than parent (left of parent)
            if p.value < n.value:
                p.right = None
                # If larger than parent (right of parent)
            else:
                p.left = None
                # Rebalance each parent up to root
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return True

            # If there is no successor
        elif right is None:
            # If smaller than parent (left of parent)
            if p.value < n.value:
                p.right = n.left
                n.left.parent = p
            # If larger than parent (right of parent)
            else:
                p.left = n.left
                n.left.parent = p
            # Rebalance each parent up to root
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return True

            # If there is a successor
        # Set successor (s) and its parent (sp)
        elif right is not None:
            node = right
            while node is not None:
                s = node
                node = node.left
            sp = s.parent

            # If successor IS child of n and n is not root
            if sp == n and p is not None:

                s.parent = p
                # If smaller than parent (left of parent)
                if p.value < s.value:
                    p.right = s
                # If larger than parent (right of parent)
                elif p.value > s.value:
                    # Reassign children and their parents
                    p.left = s
                    s.parent = p
                s.left = n.left
                if n.left is not None:
                    n.left.parent = s
                s.right = n.right.right
                if n.right.right is not None:
                    n.right.right.parent = s
                # Rebalance each parent up to root
                while p is not None:
                    self.rebalance(p)
                    p = p.parent
                return True

            # If successor is NOT child of n
            elif sp != n and p is not None:
                if p is not None:
                    # right child
                    # Reassign children and their parents
                    if s.right is not None:
                        s.right.parent = sp
                        sp.left = s.right
                        # If smaller than parent (left of parent)
                    if p.value < s.value:
                        p.right = s
                        s.parent = p
                    # If larger than parent (right of parent)
                    elif p.value > s.value:
                        # Reassign children and their parents
                        p.left = s
                        s.parent = p
                        s.left = n.left
                        if n.left is not None:
                            n.left.parent = s
                        s.right = n.right
                        if n.right is not None:
                            n.right.parent = s
                        # Rebalance each parent up to root
                        p = sp
                        while p is not None:
                            self.rebalance(p)
                            p = p.parent
                        return True

                    # left child
                    elif p is None:
                        # Reassign children and their parents
                        p.left = s
                        s.parent = p
                        if n.right is not None:
                            n.right.parent = s
                        s.right = n.right
                    # Rebalance each parent up to root
                    p = sp
                    while p is not None:
                        self.rebalance(p)
                        p = p.parent
                    return True

        # If removing the root
        if self.root.value == node_to_remove.value:
            # Set successor (s) and its parent (sp)
            node = right
            while node is not None:
                s = node
                node = node.left

            sp = s.parent
            # If successor is child of n
            if sp == n:
                # Reassign children and their parents
                s.parent = p
                s.left = n.left
                if n.left is not None:
                    n.left.parent = s
                self.root = s
                # Rebalance each parent up to root
                p = s
                while p is not None:
                    self.rebalance(p)
                    p = p.parent
                return True
            # Check successors children and reassign
            if s.right is not None:
                s.right.parent = sp
                sp.left = s.right
            else:
                sp.left = None
            # Reassign children and their parents
            s.left = n.left
            if n.left is not None:
                n.left.parent = s
            s.right = n.right
            n.right.parent = s
            s.parent = None
            self.root = s
            # Rebalance each parent up to the root
            p = sp
            while p is not None:
                self.rebalance(p)
                p = p.parent
            return True

        return False

    def contains(self, value: object) -> bool:
        """
        Returns True if the value parameter is in the tree or False if it is not
        """
        # Create new node
        new_node = TreeNode(value)
        cur_node = self.root
        # If empty tree
        if self.root is None:
            return False
            # If root is value
        elif new_node.value == cur_node.value:
            return True
            # Traverse the tree checking < or > for value
        while cur_node.value != new_node.value:

            if new_node.value < cur_node.value:
                cur_node = cur_node.left
                if new_node.value == cur_node.value:
                    return True
            else:
                cur_node = cur_node.right
                if new_node.value == cur_node.value:
                    return True
        return False

    def inorder_helper(self, root, q):
        """
        Recursive helper for inorder_traversal
        """
        if root is None:
            return q

        self.inorder_helper(root.left, q)
        q.enqueue(root)
        self.inorder_helper(root.right, q)

        return q

    def inorder_traversal(self) -> Queue:
        """
        Perform an inorder traversal of the tree and return a Queue object that contains the values of the visited nodes, in the order they were visited. If the tree is empty, the methods should return an empty Queue
        """
        q = Queue()
        # Call recursive helper function
        return self.inorder_helper(self.root, q)

    def find_min(self) -> object:
        """
        Returns the lowest value in the tree
        """
        # Set root to cur
        cur_node = self.root
        # If empty tree
        if self.root is None:
            return None
        # Traverse to extreme left
        while cur_node is not None:
            node = cur_node
            cur_node = cur_node.left

        return node

    def find_max(self) -> object:
        """
        Returns the highest value in the tree
        """
        # Set root to cur
        cur_node = self.root
        # If empty tree
        if self.root is None:
            return None
        # Traverse to extreme right
        while cur_node is not None:
            node = cur_node
            cur_node = cur_node.right

        return node

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty, otherwise the method should return False.
        """
        # Check if root exists
        if self.root is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Removes all of the nodes from the tree.
        """
        # Set root to None, disconnecting any children
        self.root = None


# ------------------- BASIC TESTING -----------------------------------------
if __name__ == '__main__':
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        avl = AVL(case)
        print(avl)
    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        avl = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', avl)
    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL()
        for value in case:
            avl.add(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')
    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)
    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)
    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)
    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', avl, avl.root.value)
        avl.remove(avl.root.value)
        print('RESULT :', avl)
    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        for value in case[::2]:
            avl.remove(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')
    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))
    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))
    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())
    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())
    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)