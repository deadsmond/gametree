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
            parents : list
                parents of node - can be multiple, represented by list of ids
            children : list
                children of node - can be multiple, represented by list of ids
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
                'parents': [],
                'children': [],
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

    # ---------------------------------- ADD NODES ---------------------------------------------------------------------
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
        node['parents'] = [] if node.get('parents') is None else node['parents']
        node['children'] = [] if node.get('children') is None else node['children']
        node['probability'] = 1 if node.get('probability') is None else node['probability']
        node['branch'] = {} if node.get('branch') is None else node['branch']
        node['branch']['value'] = 0 if node['branch'].get('value') is None else node['branch']['value']
        node['branch']['probability'] = 0 \
            if node['branch'].get('probability') is None else node['branch']['probability']

        # add parenthood
        for parent in node['parents']:
            self._nodes[parent]['children'].append(id_)

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

    # ---------------------------------- OBJECT BASIC METHODS ----------------------------------------------------------
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

    def get_income_for_path(self, path: list) -> float:
        """
        return income for path - 'root' should be skipped!
        :param list path: list of id's you want to make path with
        """
        current_node = 'root'
        for node in path:
            if node not in self._nodes[current_node]['children']:
                raise IndexError('could not find connection from %s to %s' % (current_node, node))
            else:
                current_node = '%s' % node
        return self._nodes[current_node]['value']
    # ==================================================================================================================


# testing section
if __name__ == '__main__':

    # EXAMPLE USAGE OF GAMETREE:

    help(GameTree)

    # plant a tree
    tree = GameTree()
    # add nodes
    tree.add_node({
            'id': '1',
            'value': 2,
            'parents': ['root']
    })
    tree.add_node({
            'id': '2',
            'value': 5,
            'parents': ['root']
    })

    print('tree visualisation:\n%s\n' % tree)

    tree.calculate_leafs()
    print('tree leafs are:\n%s\n' % tree.get_leafs())

    print('tree expected value is %s\n' % tree.exp())

    path_ = ['1']
    print('tree value for path\n%s\nis %s\n' % (path_, tree.get_income_for_path(path_)))
