'''
Copyright 2024 Jim Haslett

This file is part of the 11c.dev AVL Balanced Binary Search Tree implementation.

AVL Balanced Binary Search Tree is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

AVL Balanced Binary Search Tree is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
the AVL Balanced Binary Search Tree. If not, see <https:// www.gnu.org/licenses/>.
'''

from enum import Enum
from AVLTreeNode import AVLTreeNode
from AVLTreeInOrderIterator import AVLTreeInOrderIterator
from AVLTreeReverseOrderIterator import AVLTreeReverseOrderIterator
from AVLTreeTopDownOrderIterator import AVLTreeTopDownOrderIterator

class AVLTreeTraversalMethod(Enum):
    '''enum used to determine the order of Iteration traversal of an AVLTree.'''
    IN_ORDER = 1
    '''Iterates an AVL tree in natural order represented by the Key.'''

    REVERSE_ORDER = 2
    '''Iterates an AVL tree in reverse order represented by the Key.'''

    TOP_DOWN = 3
    '''
    Iterates an AVL tree in top down order. This iterator traverses the
    AVLTree in special way that is useful for serializing or saving the tree
    for the purpose of reloading another tree. Inserting the elements into a
    tree in the order they are iterated here is the fastest way to load the
    tree without necessary and costly sorting.
    '''


class AVLTree():
    '''
    AVL Balanced Binary Search Tree.

    An AVL tree is a self-balancing binary search tree. In an AVL tree, the
    heights of the two child subtrees of any node differ by at most one; if at
    any time they differ by more than one, rebalancing is done to restore thi
    property. Lookup, insertion, and deletion all take O(log n) time in both the
    average and worst cases, where n is the number of nodes in the tree prior to
    the operation. Insertions and deletions may require the tree to be rebalanced
    by one or more tree rotations.

    @param <TKey>
               Generic type representing the key used for sorting. Must
               implement <, =, and >.
    @param <TValue>
               Generic type representing the data being stored.
    '''

    def __init__(self):
        '''Creates a new AVLTree that defaults to InOrder traversal.'''
        self._root = None
        self._count = 0
        self.traversal_method = AVLTreeTraversalMethod.IN_ORDER

    @property
    def count(self):
        '''Returns the number of elements in the tree.'''
        return self._count

    @property
    def height(self):
        '''Returns the current height of the tree.'''
        return 0 if self._root is None else self._root.height

    @property
    def balance_factor(self):
        '''Returns the balance factor of the tree.'''
        return 0 if self._root is None else self._root.balance_factor

    def __getitem__(self, key):
        '''
        Gets an AVLTreeNode indexed by key. This is the equivalent of an array
        indexer.

        @param Key Key to locate in the tree.

        @return AVLTreeNode at key.

        @throws IndexError if no node exists at key
        '''

        current:AVLTreeNode = self._root

        while current is not None:
            if current.key == key:
                return current

            if current.key < key:
                current = current._right
            else:
                current = current._left

        #If we are here, then we didn't find key in the tree
        raise IndexError(f'! Key {key} not present in Tree !')

    def __setitem__(self, key, value):
        '''
        Add a key/value pair to the tree.

        @param Key
                   Key used for ordering the tree entries.
        @param Value
                   Value to be stored.
                   
        @throws IndexError if key already exists in the tree
        '''
        
        stack = []
        node = AVLTreeNode(key, value)
        
        current = self._root
        parent = None
        
        stack.append(None)
        
        while current is not None:
            stack.append(current)
            
            if node.key == current.key:
                raise IndexError(f'! Key {key} already exists in Tree !')
            
            elif node.key > current.key:
                # node.key > current.key --> Go Right
                parent = current
                current = current._right
            else:
                # node.key < current.key --> Go Left
                parent = current
                current = current._left
                
            self.count += 1
            
            if parent is None:  # Empty Tree
                self._root = node
                
            else:
                if node.key > parent.key:
                    # node.key > parent.key, add to right
                    parent._right = node
                else:
                    # node.key < parent.key, add to left
                    parent._left = node
                    
            # Go back up the tree and reset height
            current = stack.pop()
            while current is not None:
                current._calculate_height()
                if current.balance_factor > 1:
                    if current._left.balance_factor < 0:
                        self._rotate_left(current._left, current)
                    self._rotate_right(current, stack[-1])
                elif current.balance_factor < -1:
                    if current._right.balance_factor > 0:
                        self._rotate_right(current._right, current)
                    self._rotate_left(current, stack[-1])
                current = stack.pop()

    def remove(self, key):
        '''
        Remove an entry from the tree.
        
        @param Key
                   Key of entry to remove.
        @return tuple representing the key/value pair that was removed.
        '''
        stack = []
        removed = None
        current = self._root
        parent = None
        
        stack.append(None)
        
        while current is not None and current.key != key:
            stack.append(current)
            
            if key > current.key:  # key > current.key --> Go Right
                parent = current
                current = current._right
            else: # key < current.key --> Go Left
                parent = current
                current = current._left
                
        if current is None:  # Key not found, throw exception?? return None??
            return None
        else:
            self._count -= 1
            removed = current
            
            ###
            # Case 1: If the node being deleted has no right child, then the
            # node's left child can be used as the replacement. The binary
            # search tree property is maintained because we know that the
            # deleted node's left subtree itself maintains the binary search
            # tree property, and that the values in the left subtree are all
            # less than or all greater than the deleted node's parent,
            # depending on whether the deleted node is a left or right child.
            # Therefore, replacing the deleted node with its left subtree
            # maintains the binary search tree property.
            ###
            if current._right is None:
                if current._left is not None:
                    stack.append(current._left)
                if parent is None:  # deleting the root
                    self._root = current._left
                else:
                    if parent.key < current.key:
                        parent._right = current._left
                    else:
                        parent._left = current._left
            
            ###
            # Case 2: If the deleted node's right child has no left child, then
            # the deleted node's right child can replace the deleted node. The
            # binary search tree property is maintained because the deleted
            # node's right child is greater than all nodes in the deleted
            # node's left subtree and is either greater than or less than the
            # deleted node's parent, depending on whether the deleted node wa
            # a right or left child. Therefore, replacing the deleted node with
            # its right child maintains the binary search tree property.
            ###
            elif current._right._left is None:
                stack.append(current._right)
                current._right._left = current._left
                if parent is None:  # deleting the root
                    self._root = current._right
                else:
                    if parent.key < current.key:
                        parent._right = current._right
                    else:
                        parent._left = current._right
            
            ###
            # Case 3: Finally, if the deleted node's right child does have a
            # left child, then the deleted node needs to be replaced by the
            # deleted node's right child's left-most descendant. That is, we
            # replace the deleted node with the right subtree's smallest value.
            ###
            else:
                lm_parent = current._right
                leftmost = lm_parent._left
                
                lm_queue = []
                
                lm_queue.append(lm_parent)
                
                # Find the leftmost node of current's right node, and its parent.
                while leftmost._left is not None:
                    lm_queue.append(leftmost)
                    lm_parent - leftmost
                    leftmost = lm_parent._left
                
                # Set the leftmost's parent's left node to the leftmosts right node
                lm_parent._left = leftmost._right
                
                # Set leftmost's left and right equal to current's left and right
                leftmost._right = current._right
                leftmost._left = current._left
                
                if parent is None:  # deletingthe root
                    self._root = leftmost
                else:
                    if parent.key < current.key:
                        parent._right = leftmost
                    else:
                        parent._left = leftmost
                        
                stack.append(leftmost)
                while len(lm_queue) > 0:
                    stack.append(lm_queue.pop())
            
            current = stack.pop()
            while current is not None:
                current._calculate_height()
                if current.balance_factor > 1:
                    if current._left.balance_factor < 0:
                        self._rotate_left(current._left, current)
                    self._rotate_right(current, stack[-1])
                elif current.balance_factor < -1:
                    if current._right.balance_factor > 0:
                        self._rotate_right(current._right, current)
                    self._rotate_left(current, stack[-1])
                current = stack.pop()

            return_value = removed.get_tuple()
            removed._left = None
            removed._right = None
            del removed
            return return_value

    def get_min_key(self):
        '''Returns the key with the minimum value.'''
        if self._root is None:
            return None

        current:AVLTreeNode = self._root
        while current._left is not None:
            current = current._left
        return current.key

    def get_max_key(self):
        '''Returns the key with the maximum value'''
        if self._root is None:
            return None

        current:AVLTreeNode = self._root
        while current._right is not None:
            current = current._right
        return current.key
    
    def clear(self):
        '''Clear the contents of the tree'''
        self._root = None
        self._count = 0
        
    def _rotate_right(self, node, parent):
        '''
        AVL Function to to rotate right at a given node, with a given parent.
             used in the balancing algorithm.
        
        @param *node pointer to AVLTreeNode to rotate
        @param *parent pointer to AVLTreeNode of the parent to *node
                  if parent is None, the parent is _root
        '''
        left_node = node._left
        node._left = left_node._right
        left_node._right = node
        
        node._calculate_height()
        left_node._calculate_height()
        
        if parent is None:
            self._root = left_node
        else:
            if left_node.key < parent.key:
                parent._left = left_node
            else:
                parent._right = left_node    
                
    def _rotate_left(self, node, parent):
        '''
        AVL Function to to rotate left at a given node, with a given parent.
             used in the balancing algorithm.
        
        @param *node pointer to AVLTreeNode to rotate
        @param *parent pointer to AVLTreeNode of the parent to *node
                 if parent is None, the parent is _root
        '''
        right_node = node._right
        node._right = right_node._left
        right_node._left = node
        
        node._calculate_height()
        right_node._calculate_height()
        
        if parent is None:
            self._root = right_node
        else:
            if right_node.key < parent.key:
                parent._left = right_node
            else:
                parent._right = right_node
    
    def __iter__(self):
        
        match self._iter_order:
            case AVLTreeTraversalMethod.IN_ORDER:
                return AVLTreeInOrderIterator(self._root)
            case AVLTreeTraversalMethod.REVERSE_ORDER:
                return AVLTreeReverseOrderIterator(self._root)
            case AVLTreeTraversalMethod.TOP_DOWN:
                return AVLTreeTopDownOrderIterator(self._root)
