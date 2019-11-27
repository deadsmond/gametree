

# game tree object
class GameTree:
    # procedure of printing object properties
    def __repr__(self):
        # for node in self._nodes:
        #     print(node)
        return str(self._nodes)

    # initialize object
    def __init__(self):
        self._nodes = {
            'root': {
                'id': 'root',
                'value': 0,
                'parents': {},
                'children': {},
                'probability': 1
            }
        }
        # list of lists of knowledge groups
        self._groups = []

    # add node method
    def add_node(self, node, override=False):
        # check if it is not overriding existing node
        if node['id'] in self._nodes and not override:
            raise ValueError('wrong id of node with no override permission')
        # add node
        self._load_node_data(node)

    def _load_node_data(self, node):
        # append node to list
        self._nodes[node.id] = node
        # add parenthood
        self._nodes[node.parents]['children'] = node

        # calculate total probability of node

        # calculate total node's value

    def get_leafs(self):
        return dict(node['id'] for node in self._nodes if not node['children'])


# testing section
if __name__ == '__main__':
    # plant a tree
    tree = GameTree()
    # add nodes
    tree.add_node(
        {
            'id': '1',
            'value': 2,
            'parents': {'root'},
            'children': {},
            'probability': 1
        }
    )
    tree.add_node(
        {
            'id': '2',
            'value': 5,
            'parents': {'root'},
            'children': {},
            'probability': 1
        }
    )

    print(tree)
