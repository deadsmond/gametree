import json


# ======================================================================================================================
# game tree object
class GameTree:
    # ---------------------------------- OBJECT PROPERTIES -------------------------------------------------------------
    # procedure of printing object properties
    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

    # initialize object
    def __init__(self, nodes: dict = None, groups: list = None, leafs: list = None):
        """
        GameTree class used to represent game tree:

        Attributes
        ----------
        nodes : dict
            dictionary of nodes;
        groups : list
            list of groups
        leafs : list
            list of leafs, calculated on demand
        """

        '''
        dictionary of nodes:
        Attributes
        ----------
        node : dict
            dictionary representing node;

            Attributes
            ----------
            value : float
                value of node (the prize for reaching the node)
            parents : dict
                parents of node - can be multiple, represented by dict of ids and connection values
            children : dict
                children of node - can be multiple, represented by dict of ids and connection values
            probability : float
                probability of node - 1 means there is no random choice
            branch : dict
                totals of branch, to avoid tree walking

                Attributes
                ----------
                value : float
                    total value of branch
                probability : float
                    probability of reaching this node in game
        '''
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
        } if nodes is None else nodes
        # list of lists of knowledge groups
        self._groups = [] if groups is None else groups
        # dictionary of leafs
        self._leafs = [] if leafs is None else leafs

    # ---------------------------------- NODES -------------------------------------------------------------------------
    def add_node(self, node: dict, override=False):
        """
        add node method. Runs basic validation before adding.

        :param dict node: dictionary of node's data
        :param bool override: control variable allowing to overwrite node
        """
        # check if it is not overriding existing node
        if node.get('id') is not None:
            if node['id'] in self._nodes and not override:
                raise ValueError('wrong id of node with no override permission')
        else:
            raise ValueError('no id for node provided')

        # append node to list
        id_ = node['id']
        del node['id']

        # set default values for node
        node['value'] = 0 if node.get('value') is None else node['value']
        node['parents'] = {} if node.get('parents') is None else node['parents']
        node['children'] = {} if node.get('children') is None else node['children']
        node['probability'] = 1 if node.get('probability') is None else node['probability']
        node['branch'] = {} if node.get('branch') is None else node['branch']
        node['branch']['value'] = 0 if node['branch'].get('value') is None else node['branch']['value']
        node['branch']['probability'] = 0 \
            if node['branch'].get('probability') is None else node['branch']['probability']

        # add parenthood
        for parent in node['parents']:
            # noinspection PyTypeChecker
            self._nodes[parent]['children'][id_] = str(node['parents'][parent])

        # calculate total probability of node:
        # total probability equals sum of probabilities of parents multiplied by probability of node
        branch_probability = 0
        for parent in node['parents']:
            branch_probability += self._nodes[parent]['branch']['probability']
        node['branch']['probability'] = branch_probability * node['probability']

        # calculate total node's value - sum of all previous totals: TODO? does this make sense?
        branch_value = 0
        for parent in node['parents']:
            branch_value += self._nodes[parent]['branch']['value']
        node['branch']['value'] = branch_value + node['value']

        # add node
        self._nodes[id_] = node

    def copy_node(self, from_: str, to_: str):
        """
        create a copy of node's properties in another node

        :param str from_: origin node of properties
        :param str to_: destination node for properties
        """
        self._nodes[to_] = dict(self._nodes[from_])

    # ---------------------------------- OBJECT BASIC METHODS ----------------------------------------------------------
    @staticmethod
    def _get_key(obj: dict, val: str) -> list:
        """
        get list of keys with specified value from obj dictionary
        :param dict obj: chosen dictionary
        :param str val: specified value
        """
        sublist = [key for (key, value) in obj.items() if value == val]
        if sublist:
            return sublist
        else:
            raise ValueError('key with value %s does not exist in %s' % (val, obj))

    # -------------- LEAFS -------------
    def calculate_leafs(self):
        """ calculate inner list of leafs ids """
        self._leafs = [node for node in self._nodes if not self._nodes[node]['children']]

    def get_leafs(self) -> list:
        """ return list of leafs ids """
        return self._leafs[:]

    # -------------- GROUPS ------------
    def set_group(self, group: list):
        """
        add list of ids to new group
        :param list group: list of id's you want to create group with
        """
        self._groups.append(group)

    def get_groups(self) -> list:
        """ return list of groups """
        return self._groups[:]

    # ---------------------------------- TREE CALCULATIONS -------------------------------------------------------------
    def exp(self) -> float:
        """ return expected value of tree """
        # collect leafs
        self.get_leafs()

        exp = 0
        # calculate expected value
        for leaf in self._leafs:
            exp += self._nodes[leaf]['branch']['value'] * self._nodes[leaf]['branch']['probability']
        return exp / len(self._leafs)

    def get_income_for_path(self, path: list, mode: str = 'nodes') -> float:
        """
        return income for path - 'root' should be skipped!
        :param list path: list of id's you want to make path with
        :param str mode: mode of search, 'nodes' - search path via nodes id, 'moves' - search path via player choices
        """
        if mode == 'nodes':
            current_node = 'root'
            for node in path:
                if node not in self._nodes[current_node]['children']:
                    raise IndexError('could not find connection from %s to %s' % (current_node, node))
                else:
                    current_node = '%s' % node

        elif mode == 'moves':
            current_node = 'root'
            for val in path:
                key = self._get_key(obj=self._nodes[current_node]['children'], val=val)
                current_node = '%s' % key[0]
        else:
            raise ValueError('mode variable is not "nodes" nor "moves"')
        return self._nodes[current_node]['value']
    # ==================================================================================================================


# EXAMPLE USAGE OF GAME TREE:
if __name__ == '__main__':

    # print documentation of class
    help(GameTree)

    # plant a tree
    tree = GameTree()
    # add nodes
    tree.add_node({
            'id': '1',
            'parents': {'root': 'L'}
    })
    tree.add_node({
            'id': '2',
            'parents': {'root': 'P'}
    })
    tree.add_node({
        'id': '3',
        'value': 2,
        'parents': {'1': 'a'}
    })
    tree.add_node({
        'id': '4',
        'value': 1,
        'parents': {'1': 'b'}
    })
    tree.add_node({
        'id': '5',
        'value': 1,
        'parents': {'2': 'a'}
    })
    tree.add_node({
        'id': '6',
        'parents': {'2': 'b'}
    })
    tree.add_node({
        'id': '7',
        'parents': {'6': 'L'}
    })
    tree.add_node({
        'id': '8',
        'parents': {'6': 'P'}
    })
    tree.add_node({
        'id': '9',
        'value': 2,
        'parents': {'7': 'L'}
    })
    tree.add_node({
        'id': '10',
        'value': 1,
        'parents': {'7': 'P'}
    })
    tree.add_node({
        'id': '11',
        'value': -2,
        'parents': {'8': 'L'}
    })
    tree.add_node({
        'id': '12',
        'value': 3,
        'parents': {'8': 'P'}
    })

    # add groups
    tree.set_group(['1', '2'])
    tree.set_group(['7', '8'])

    # tests:
    # print
    print('tree visualisation:\n%s\n' % tree)

    # leafs:
    tree.calculate_leafs()
    print('tree leafs are:\n%s\n' % tree.get_leafs())

    # value of tree
    print('tree expected value is %s\n' % tree.exp())

    # paths:
    # correct path example - nodes
    path_ = ['2', '6', '8', '12']
    print('tree value for path\n%s\nis %s\n' % (path_, tree.get_income_for_path(path_)))

    # correct path example - moves
    path_ = ['P', 'b', 'L', 'P']
    print('tree value for path\n%s\nis %s\n' % (path_, tree.get_income_for_path(path=path_, mode='moves')))

    # wrong path example - no connection between 5 and 8
    path_ = ['2', '5', '8', '12']
    try:
        print('tree value for path\n%s\nis %s\n' % (path_, tree.get_income_for_path(path_)))
    except IndexError as e:
        print(e)
