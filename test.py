'''Script for testing and verifying proper functionality of the AVL Tree'''

from AVLTree import AVLTree, AVLTreeTraversalMethod
import random


tree = AVLTree()

print('Simple Insert Testing:')

tree[0] = 'zero'

print(tree[0])

for item in tree:
    print(item)
    
print('Clear Testing:')

tree.clear()
# print(f'Items in tree = {tree.count}')
print(f'Items in tree = {len(tree)}')
for item in tree:
    print(item)


print('Update Value Testing')

test = tree.get(10, [])
print('test =', test)
test.append('Ten')
print('test =', test)
tree[10] = test
print(f'tree[10] = {tree[10]},  len(tree) = {len(tree)}')

tree[10] = ['ten']
print(f'tree[10] = {tree[10]},  len(tree) = {len(tree)}')


tree[10].append('Ten')
print(f'tree[10] = {tree[10]},  len(tree) = {len(tree)}')


print('Random Insert Testing:')

tree.clear()
orig = []

for i in range(100000):
    r = random.randint(-10000000, 10000000)
    orig.append(r)
    tree[r] = r
    
control = list(set(orig))
control.sort()

if len(control) != len(tree):
    print(f'Lengths don\'t match:  control = {len(control)}, tree = {len(tree)}')

tree.traversal_method = AVLTreeTraversalMethod.IN_ORDER
i = 0
OK = True
for i, item in enumerate(tree):
    if control[i] != item[0]:
        print(f'Values don\'t match!  i={i}, control[{i}] = {control[i]}, item={item[0]}')
        
        OK = False
        break
    
if OK:
    print(f'All {len(tree)} items matched')
else:
    stop = False
    for i, item in enumerate(tree):
        print(f'{control[i]}  {item[0]}')
        if stop:
            break
        if control[i] != item[0]:
            print(f'{item[0]} is in orig: {item[0] in orig}')
            stop = True

print('\n')
    