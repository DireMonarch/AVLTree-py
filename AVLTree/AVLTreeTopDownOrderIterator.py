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

class AVLTreeTopDownOrderIterator(AVLTreeIterator):
    '''
    Iterates an AVL tree in top down order. This iterator traverses the AVLTree
    in special way that is useful for serializing or saving the tree for the
    purpose of reloading another tree. Inserting the elements into a tree in the
    order they are iterated here is the fastest way to load the tree without
    necessary and costly sorting.
    
    @author Jim Haslett
    @since Feb 12, 2025 (translated from the original Java 2013 version)
    @param <TKey>
               Generic type representing the key used for sorting. Must be
               Comparable.
    @param <TValue>
               Generic type representing the data being stored.
    '''
    
    def __init__(self, root):
        AVLTreeIterator.__init__(self, root)
        self.queue = []
        
    def _move_next(self):
        '''
        Moves the current pointer to the next element. The next element is
        determined by the traversal method.
        
        @return True if MoveNext was successful and there was a valid element to
                move to, otherwise false.
        @throws Exception
        '''
                
        if self._status == AVLTreeIterator.StatusEnum.INVALID:
            raise Exception('! AVL Tree has changed, this enumerator is no longer valid !')
        
        if self._status == AVLTreeIterator.StatusEnum.BEFORE_FIRST:
            if self._root is not None:
                self.queue.clear()
                self.queue.append(self._root)
                self._status = AVLTreeIterator.StatusEnum.OK
            else:
                self._status = AVLTreeIterator.StatusEnum.AFTER_LAST
                self.queue.clear()
                self._current = None
                return False
        elif self._status == AVLTreeIterator.StatusEnum.AFTER_LAST:
            self._current = None
            self.queue.clear()
            return False
        
        if len(self.queue) > 0:
            self._current = self.queue.pop(0)  # POP first element
            if self._current._left is not None:
                self.queue.append(self._current._left)
            if self._current._right is not None:
                self.queue.append(self._current._right)
        else:
            self._status = AVLTreeIterator.StatusEnum.AFTER_LAST
            self.queue.clear()
            return False
        
        return True
        