import json


# game tree object
class GameTree:
    # procedure of printing object properties
    def __repr__(self):
        # return json.dumps(self.__dict__)
        return json.dumps(self.__dict__, indent=4)

    # initialize object
    def __init__(self):
        self._nodes = {
            'root': {
                'value': 0,
                'parents': {},
                'children': {},
                'probability': 1,
                'branch': {
                    'value': 0,
                    'probability': 1
                }
            }
        }
        # list of lists of knowledge groups
        self._groups = []
        # dictionary of leafs
        self._leafs = []

    # add node method
    def add_node(self, node: dict, override=False):
        # check if it is not overriding existing node
        if node.get('id') is not None:
            if node['id'] in self._nodes and not override:
                raise ValueError('wrong id of node with no override permission')
        else:
            raise ValueError('no id for node provided')

        # add node:
        # append node to list
        id_ = node['id']
        del node['id']

        # default values for node
        node['value'] = 0 if node.get('value') is None else node['value']
        node['parents'] = {} if node.get('parents') is None else node['parents']
        node['children'] = {} if node.get('children') is None else node['children']
        node['probability'] = 1 if node.get('probability') is None else node['probability']
        node['branch'] = {} if node.get('branch') is None else node['branch']
        node['branch']['value'] = 0 if node['branch'].get('value') is None else node['branch']['value']
        node['branch']['probability'] = 0 \
            if node['branch'].get('probability') is None else node['branch']['probability']

        self._nodes[id_] = node
        # add parenthood
        for parent in node['parents']:
            self._nodes[parent]['children'] = node

        # calculate total probability of node

        # calculate total node's value

    # return list of leafs
    def get_leafs(self):
        self._leafs = [node for node in self._nodes if not self._nodes[node]['children']]


# testing section
if __name__ == '__main__':

    # plant a tree
    tree = GameTree()
    # add nodes
    tree.add_node({
            'id': '1',
            'value': 2,
            'parents': {'root'}
    })
    tree.add_node({
            'id': '2',
            'value': 5,
            'parents': {'root'}
    })

    # WTF TODO
    # print(tree)
