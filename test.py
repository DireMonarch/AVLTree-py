'''Script for testing and verifying proper functionality of the AVL Tree'''

from AVLTree import AVLTree, AVLTreeTraversalMethod
import random


tree = AVLTree()

print('Simple Insert Testing:')

tree[0] = 'zero'

print(tree[0].value)

for item in tree:
    print(item)
    
print('Clear Testing:')

tree.clear()
# print(f'Items in tree = {tree.count}')
print(f'Items in tree = {len(tree)}')
for item in tree:
    print(item)
    
print('Random Insert Testing:')

control = []

for i in range(10):
    r = random.randint(-1000, 1000)
    print(r)
    control.append(r)
    tree[r] = r
    

control.sort()
print(control)
tree.traversal_method = AVLTreeTraversalMethod.TOP_DOWN
for item in tree:
    print(item[0], end=' ')

print('\n')
    