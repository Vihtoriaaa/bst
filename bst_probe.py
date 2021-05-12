"""
File: bst_probe.py
A tester program for binary search trees.
"""
from linkedbst import LinkedBST
import random


def main():

    tree = LinkedBST()
    print("Adding D B A C F E G")
    tree.add("D")
    tree.add("B")
    tree.add("A")
    tree.add("C")
    tree.add("F")
    tree.add("E")
    tree.add("G")

    print("\nExpect True for A in tree: ", "A" in tree)

    print("\nString:\n" + str(tree))

    clone = LinkedBST(tree)
    print("\nClone:\n" + str(clone))
    
    print("Expect True for tree == clone: ", tree == clone)

    print("\nFor loop: ", end="")
    for item in tree:
        print(item, end=" ")

    print("\n\ninorder traversal: ", end="")
    for item in tree.inorder(): print(item, end = " ")
    
    #print("\n\npreorder traversal: ", end="")
    #for item in tree.preorder(): print(item, end = " ")
    
    #print("\n\npostorder traversal: ", end="")
    #for item in tree.postorder(): print(item, end = " ")
    
    #print("\n\nlevelorder traversal: ", end="")
    #for item in tree.levelorder(): print(item, end = " ")

    print("\n\nRemoving all items:", end = " ")
    for item in "ABCDEFG":
        print(tree.remove(item), end=" ")

    print("\n\nExpect 0: ", len(tree))

    tree = LinkedBST(range(1, 16))
    print("\nAdded 1..15:\n" + str(tree))
    
    lyst = list(range(1, 16))

    random.shuffle(lyst)
    tree = LinkedBST(lyst)
    print("\nAdded ", lyst, "\n" + str(tree))


    lyst = [113,30,68,74,45,91,88]
    #random.shuffle(lyst)
    tree = LinkedBST(lyst)
    print(tree, tree.height())
    print(tree.isBalanced())
    print(tree.rangeFind(30,91))
    print(tree.successor(20))
    print(tree.predecessor(50))
    tree.rebalance()
    print(tree)
   #print("\nAdded ", lyst, "\n" + str(tree))
   # tree.remove(10)
    #print("\nAdded ", lyst, "\n" + str(tree))
    #tree.remove(12)
    #print("\nAdded ", lyst, "\n" + str(tree))


    
if __name__ == "__main__":
    main()



