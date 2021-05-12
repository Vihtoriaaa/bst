"""linkedbst.py module yesss!!!"""
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import ceil, log
import random
from time import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while node is not None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node = self._root

            while True:
                # New item is less, go left until spot is found
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
                    # End of recurse
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        def lift_max_in_left_subtree_to_top(top):
            """Helper function to adjust placement of an item"""
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height_recursion(top):
            '''
            Helper function
            :param to
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height_recursion(top.right), \
                    height_recursion(top.left))

        return height_recursion(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = []
        all_items = self.inorder()
        for item in list(all_items):
            if item >= low and item <= high:
                result.append(item)
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        items = list(self.inorder())
        self.clear()

        def help_rebalance(tree_list):
            if len(tree_list) == 0:
                return

            middle_pos = ceil((len(tree_list) - 1) / 2)
            self.add(tree_list[middle_pos])
            help_rebalance(tree_list[:middle_pos])
            help_rebalance(tree_list[middle_pos + 1:])

        help_rebalance(items)

    def successor(self, item_to_search):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        all_items = self.inorder()
        for item in list(all_items):
            if item > item_to_search:
                result.append(item)
        if len(result) == 0:
            return None

        return result[0]

    def predecessor(self, item_to_search):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        all_items = self.inorder()
        for item in list(all_items):
            if item < item_to_search:
                result.append(item)
        if len(result) == 0:
            return None

        return result[-1]

    def demo_bst(self, path: str):
        """Demonstration of efficiency binary search tree for the search
        tasks."""

        def get_info(path: str):
            with open(path) as file:
                all_lines = file.read().splitlines()
            return all_lines

        all_info = get_info(path)  # our info is list with all file words

        def get_random_words(info: list):
            """Retuns a list with 10 000 random words from a file."""
            result = []
            for _ in range(10000):
                result.append(random.choice(info))
            return result

        def sorted_words(info: list):
            """Retuns a list with 10 000 alphabet sorted words from a list
            with words."""
            result = list()
            for ind in range(10000):
                result.append(info[ind])
            return result

        def find_random_words(all_info: list):
            """Retuns time for searching 10 000 random words from a list with
            words."""
            rand_words = get_random_words(all_info)
            start_time = time()

            for word in rand_words:
                word in rand_words

            finish_time = time() - start_time
            print(f'Search time for random words in list: \
{format(finish_time, ".5f")} sec')

        def random_tree_find(all_info: list):
            """Retuns time for searching 10 000 random words in a BST."""
            tree = LinkedBST()
            rand_words = get_random_words(all_info)
            for word in rand_words:
                tree.add(word)

            start_time = time()

            for word in rand_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for random words in BST: \
{format(finish_time, ".5f")} sec')

        def balanced_random_tree_find(all_info: list):
            """Retuns time for searching 10 000 random words in a balanced
            BST."""
            tree = LinkedBST()
            rand_words = get_random_words(all_info)
            for word in rand_words:
                tree.add(word)

            tree.rebalance()
            start_time = time()

            for word in rand_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for random words in balanced BST: \
{format(finish_time, ".5f")} sec')

        def create_alphabet_tree(all_info: list):
            """Retuns time for searching 10 000 alphabet sorted words
            in a BST."""
            tree = LinkedBST()
            sort_words = sorted_words(all_info)
            for word in sort_words:
                tree.add(word)

            start_time = time()

            for word in sort_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for alphabet sorted words in BST: \
{format(finish_time, ".5f")} sec')

        # function calling
        find_random_words(all_info)
        random_tree_find(all_info)
        balanced_random_tree_find(all_info)
        create_alphabet_tree(all_info)

if __name__ == "__main__":
    tree = LinkedBST()
    tree.demo_bst('words.txt')

