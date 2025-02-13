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
the AVL Balanced Binary Search Tree. If not, see <https://www.gnu.org/licenses/>.
'''


class AVLTreeNode():
    '''
    Node used in an AVLTree.

    @param <TKey>	Generic type representing the key used for sorting.  Must implement <, =, and >.
    @param <TValue>	Generic type representing the data being stored.
    '''

    def __init__(self, key, value):
        '''
        Creates a leaf node with no left or right children.

        @param Key		Key used for sorting.  Must be Comparable.
        @param Value		Data being stored in the Tree.
        '''
        self._key = key
        self.value = value
        self._left = None
        self._right = None
        self._calculate_height()


    @property
    def key(self):
        '''
        Returns the key of the tree node.

        This is done this way as a tiny bit of protection agains accidently modifying
        the key, which would, in all likelyhood, destroy the ordering of the tree.  If
        Python had private variables, _key would be one for sure!
        '''
        return self._key


    def _calculate_height(self):
        '''Recalcualtes the height of the node'''
        r = -1 if self._right is None else self._right.height
        l = -1 if self._left is None else self._left.height
        self.height = r + 1 if r > l else l + 1


    @property
    def balance_factor(self):
        '''
        Get the balance factor of the current node.

        Compares height if right and left child nodes.
        Used to determine how balanced this node is.

        @return	Balance factor of the node.
        '''
        r = -1 if self._right is None else self._right.height
        l = -1 if self._left is None else self._left.height
        return l - r

    def get_tuple(self):
        '''Returns a simple key, value pair tuple'''
        return (self._key, self.value)
