"""
Copyright 2019 by Adam Lewicki
This file is part of the Game Theory library,
and is released under the "MIT License Agreement". Please see the LICENSE
file that should have been included as part of this package.
"""
import json
from operator import add


# ======================================================================================================================
# game tree object
class GameTree:
    # ---------------------------------- OBJECT PROPERTIES -------------------------------------------------------------
    # procedure of printing object properties
    def __repr__(self):
        """ return tree as JSON serialized dictionary """
        return self.pretty_print(self.__dict__)

    @staticmethod
    def pretty_print(dictionary: dict):
        """ return pretty printed dictionary as JSON serialized object """
        return json.dumps(dictionary, indent=4)

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

        # remember to add new attributes to add_node method default values setting
        self._nodes = {
            'root': {
                'player': '1',
                'value': [0, 0],
                'parents': {},
                'children': {},
                'probability': 1,
                'branch': {
                    'probability': 1
                },
                'depth': 0
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
                raise ValueError('tried to override node %s without permission' % node['id'])
        else:
            raise ValueError('no id for node provided')

        # append node to list
        id_ = node['id']
        del node['id']

        # set default values for node
        # remember to add new attributes here and in __init__ root node
        node['player'] = '0' if node.get('player') is None else node['player']
        node['value'] = [0, 0] if node.get('value') is None else node['value']
        node['parents'] = {} if node.get('parents') is None else node['parents']
        node['children'] = {} if node.get('children') is None else node['children']
        node['probability'] = 1 if node.get('probability') is None else node['probability']
        node['branch'] = {} if node.get('branch') is None else node['branch']
        node['branch']['probability'] = 0 \
            if node['branch'].get('probability') is None else node['branch']['probability']

        # add parenthood
        for parent in node['parents']:
            # noinspection PyTypeChecker
            self._nodes[parent]['children'][id_] = str(node['parents'][parent])

        # set depth to one more than first parent
        print(id_)
        if node['parents']:
            node['depth'] = self._nodes[str(list(node['parents'].keys())[0])]['depth'] + 1
        else:
            node['depth'] = 0 if node.get('depth') is None else node['depth']

        # calculate total probability of node:
        # total probability equals sum of probabilities of parents multiplied by probability of node
        branch_probability = 0
        for parent in node['parents']:
            branch_probability += self._nodes[parent]['branch']['probability']
        node['branch']['probability'] = branch_probability * node['probability']

        # add node
        self._nodes[id_] = node

    def copy_node(self, from_: str, to_: str):
        """
        create a copy of node's properties in another node

        :param str from_: origin node of properties
        :param str to_: destination node for properties
        """
        self._nodes[to_] = dict(self._nodes[from_])

    def change_node(self, node: dict):
        """
        change node method. Changes attributes provided in node dictionary

        :param dict node: dictionary of node's data
        """
        # check if it is not overriding existing node
        if node.get('id') is not None:
            if node['id'] not in self._nodes:
                raise ValueError('tried to change non-existing node %s' % node['id'])
        else:
            raise ValueError('no id for node provided')

        # change attributes
        id_ = node['id']
        del node['id']
        for attribute in node:
            self._nodes[id_][attribute] = node[attribute]

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
    def exp(self) -> list:
        """ return expected value of tree """
        # collect leafs
        self.get_leafs()

        exp = self._nodes['root']['value']
        # calculate expected value
        for leaf in self._leafs:
            exp = list(map(add, exp,
                           [x * self._nodes[leaf]['branch']['probability'] for x in self._nodes[leaf]['value']]
                           ))
        return [x / len(self._leafs) for x in exp]

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

    def get_income_for_leafs(self) -> dict:
        """
        return dictionary of income for leafs
        """
        # get leafs
        self.calculate_leafs()
        result = {}
        for leaf in self._leafs:
            result[leaf] = self._nodes[leaf]['value']
        return result
    # ==================================================================================================================


# EXAMPLE USAGE OF GAME TREE:
if __name__ == '__main__':
    # -------------------------------------------- INIT ----------------------------------------------------------------
    # plant a tree
    tree = GameTree()
    # add nodes
    tree.add_node({
            'id': '1',
            'player': '2',
            'parents': {'root': 'L'}
    })
    tree.add_node({
            'id': '2',
            'player': '2',
            'parents': {'root': 'P'}
    })
    tree.add_node({
        'id': '3',
        'value': [2, 1],
        'parents': {'1': 'a'}
    })
    tree.add_node({
        'id': '4',
        'value': [1, -1],
        'parents': {'1': 'b'}
    })
    tree.add_node({
        'id': '5',
        'value': [1, 1],
        'parents': {'2': 'a'}
    })
    tree.add_node({
        'id': '6',
        'player': '1',
        'parents': {'2': 'b'}
    })
    tree.add_node({
        'id': '7',
        'player': '2',
        'parents': {'6': 'L'}
    })
    tree.add_node({
        'id': '8',
        'player': '2',
        'parents': {'6': 'P'}
    })
    tree.add_node({
        'id': '9',
        'value': [2, 3],
        'parents': {'7': 'L'}
    })
    tree.add_node({
        'id': '10',
        'value': [1, 2],
        'parents': {'7': 'P'}
    })
    tree.add_node({
        'id': '11',
        'value': [-2, 3],
        'parents': {'8': 'L'}
    })
    tree.add_node({
        'id': '12',
        'value': [3, 3],
        'parents': {'8': 'P'}
    })

    # add groups
    tree.set_group(['1', '2'])
    tree.set_group(['7', '8'])
    # -------------------------------------------- TESTS ---------------------------------------------------------------
    # tests:
    # print documentation of class
    help(GameTree)

    # overwrite node - not accepted: node exists, and override variable is false
    try:
        tree.add_node({
            'id': '12',
            'value': [-300, 0]
        })
    except ValueError as e:
        print(e, '\n')

    # change node with add method and true override
    tree.add_node({
        'id': '12',
        'value': [-300, 0]
    }, override=True)

    # change node with change method
    tree.change_node({
        'id': '12',
        'value': [-300, 0]
    })

    # reverse changes - for game purpose
    tree.change_node({
        'id': '12',
        'value': [3, 3]
    })

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

    # get dictionary of income per leaf
    print('\nvalues per leaf:')
    print(tree.pretty_print(tree.get_income_for_leafs()))
