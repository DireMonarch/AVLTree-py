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
from AVLTreeIterator import AVLTreeIterator

class AVLTreeReverseOrderIterator(AVLTreeIterator):
    '''
    Iterates an AVL tree in reverse order represented by the Key.  This iterator traverses the AVLTree in the reverse order as determined by comparing TKey.
    
    @author Jim Haslett
    @since Feb 12, 2025 (translated from the original Java 2013 version)
    @param <TKey>	Generic type representing the key used for sorting.  Must be Comparable.
    @param <TValue>	Generic type representing the data being stored.
    '''
    
    def _move_next(self):
        '''
        Moves the current pointer to the next element. The next element is
        determined by the traversal method.
        
        @return True if MoveNext was successful and there was a valid element to
                move to, otherwise false.
        @throws Exception
        '''
        if self._status == AVLTreeIterator.StatusEnum.INVALID:
            raise Exception('! AVL Tree has changed, this Iterator is no longer valid !')
        
        if self._status == AVLTreeIterator.StatusEnum.BEFORE_FIRST:
            if self._root is not None:
                self._stack.clear()
                self._stack.append(None)
                self._stack.append(self._root)
                self._stack_right_to_null()
                self._status = AVLTreeIterator.StatusEnum.OK
            else:
                self._status = AVLTreeIterator.StatusEnum.AFTER_LAST
                self._stack.clear()
                self._current = None
                return False
        
        elif self._status == AVLTreeIterator.StatusEnum.AFTER_LAST:
            self._current = None
            self._stack.clear()
            return False
        elif self._current._left is not None:
            self._stack.append(self._current._left)
            self._stack_right_to_null()
        
        self._current = self._stack.pop()
        if self._current is None:
            self._status = AVLTreeIterator.StatusEnum.AFTER_LAST
            self._stack.clear()
            return False
        
        return True
    
    def _stack_right_to_null(self):
        '''Helper function that adds all right nodes, from the node on the top of the stack, onto the stack'''
        current = self._stack[-1]
        if current is None:
            raise Exception('! Internal error: Invalid stack operation !')
        current = current._right
        while current is not None:
            self._stack.append(current)
            current = current._right        