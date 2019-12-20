# gametree
object for game theory tree implementation.

---
## Example

Example is available after running `python gametree.py` in terminal. 
Example will create tree as shown below:

![no tree picture found in documents folder](documents/example_tree.png)

Any additional help can be called via `help(GameTree)` inside script or found in comments.

---
## Functions
### Creation and manipulation of tree
* create tree object: `tree = GameTree()`
* add node:

        tree.add_node({
            'id': '3',
            'value': [2, 1],
            'parents': {'1': 'a'}
        })
        
        
This method will raise `ValueError`, if node with ID exists.
To overwrite existing node, please method `change_node`.

* add_vertex:

Simplified version of add_node. Calling:

    tree.add_vertex('12', '2', {'8' : 'P'})

results in subcall of:

    tree.add_node({
        'id': '12',
        'player':'2',
        'parents': {'8': 'P'}
    })
    
* add_leaf:

Simplified version of add_node. Calling:

    tree.add_leaf('12', [-7, 6], {'8' : 'P'})

results in subcall of:

    tree.add_node({
        'id': '12',
        'value': [-7, 6],
        'parents': {'8': 'P'}
    })
    
* change node with change method:

        tree.change_node({
            'id': '3',
            'value': [-300, 0]
        })
        
    Method will overwrite properties provided in dictionary, leaving other properties of node unchanged.

* add information set:
 
 (id of group, id of player owning the group, list of nodes in group)

        tree.set_group('A1', '1', [1', '2'])
        
* get information sets for tree:

        tree.get_groups()
        
* get information sets for specific player ('1', for example):

        tree.get_groups_of_player('1')
    
* print documentation of class
    
        help(GameTree)

* get tree as JSONified text:

        print(tree)

### Leafs
* populate list of leafs - not done automatically, as in big trees can kill performance:
        
        tree.calculate_leafs()
        
* get list of leafs from tree:
    
        print(tree.get_leafs())

### Income

**WARNING** - this section is experimental as it has not been checked and proved mathematically.

GameTree provides function for the return of income for players - `get_income_for_path`.
This method contains two arguments: path and mode for search. Mode can have two values: `nodes` or `moves`.
`nodes` allows to search via nodes IDs, moves - via player's choices.

Default mode value is `nodes`.

Method will raise `IndexError`, if there is no connection between nodes in provided path.

* get list of income for players via nodes ID' path

        path_ = ['2', '6', '8', '12']
        print('tree value for path\n%s\nis %s\n' % (
            path_, 
            tree.get_income_for_path(path_)
            )
        )

* get list of income for players via players moves' path

        path_ = ['P', 'b', 'L', 'P']
        print('tree value for path\n%s\nis %s\n' % (
            path_, 
            tree.get_income_for_path(
                path=path_,
                mode='moves'
                )
            )
        )


* get dictionary of income per leaf

        print(tree.get_income_for_leafs())
        
### Solving game

* get expected value of tree:

        print(tree.exp())

* get game optimal path and result via reversed analysis

        print(tree.reversed_analysis())
        
This method contains argument 'mode' for search. 
Mode can have two values: `nodes` or `moves`. `nodes` returns path via nodes IDs, `moves` - via player's choices.

Default mode value is `nodes`.

---
# Warnings

Due to the lack of required support, minor differences between README file 
and actual state of GameTree may appear.

Please keep in mind that not all functions had been explained in README.

We are sorry for any inconvenience.

---
*Adam Lewicki, December 2019*

