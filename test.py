# test script
from gametree_lite import GameTree


if __name__ == '__main__':
    tree = GameTree()
    tree.add_node({
                'id': 'A',
                'player': '2',
                'parents': {'root': 'L'}
        })
    tree.add_node({
        'id': '10',
        'value': [1, 2],
        'parents': {'A': 'P'}
    })
    tree.calculate_leafs()
    print(tree.get_leafs())
