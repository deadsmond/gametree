# test script
from gametree import GameTree


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
    print(tree)

    tree.calculate_leafs()
    print(tree.get_leafs())
