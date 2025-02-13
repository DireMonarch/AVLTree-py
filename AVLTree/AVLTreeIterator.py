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


class AVLTreeIterator():
    '''
    Abstract base class for all AVL Tree Iterators.
    
    @author Jim Haslett
    @since Feb 12, 2025 (translated from the original Java 2013 version)
    @param <TKey>
               Generic type representing the key used for sorting. Must be
               Comparable.
    @param <TValue>
               Generic type representing the data being stored.
    '''
    class StatusEnum(Enum):
        '''Enum used to track Iterator status'''
        OK = 0
        BEFORE_FIRST = 1
        AFTER_LAST = 2
        INVALID = 3
        
    def __init__(self, root:AVLTreeNode):
        '''
        Constructor.
         
        @param Root
                    AVLTreeNode where the iteration will start.
        @throws Exception
        '''
        self._current = None
        self._status = AVLTreeIterator.StatusEnum.BEFORE_FIRST
        self._stack = []
        self._root = root
        
        self._move_next()
        
    def _move_next(self):
        '''
        Moves the current pointer to the next element. The next element is
        determined by the traversal method.
        
        @return True if MoveNext was successful and there was a valid element to
                move to, otherwise false.
        @throws Exception
        '''
        pass
    
    def __next__(self):
        '''
        Returns the current element in the iteration.
        
        @return The TValue element at the current pointer location.
        @throws Exception
        '''
        if self._status == AVLTreeIterator.StatusEnum.OK or self._status == AVLTreeIterator.StatusEnum.INVALID:
            return_value = self._current.get_tuple()
            self._move_next()
            return return_value
        if self._status == AVLTreeIterator.StatusEnum.BEFORE_FIRST:
            raise Exception('! Before first element of AVL Search Tree, Call MoveNext first !')
        if self._status == AVLTreeIterator.StatusEnum.AFTER_LAST:
            raise Exception('! After Last element of AVL Search Tree !')
        raise Exception('! Unknown Status during iteration !')
        