from base_player import BasePlayer
import networkx as nx

class Player(BasePlayer):

    SPREAD = 0
    ATTACK_1 = 1
    ATTACK_2 = 2
    ATTACK_3 = 3
    DEFEND_1 = 4
    DEFEND_2 = 5
    DEFEND_3 = 6
    IDEFEND_1 = 7
    IDEFEND_2 = 8
    IDEFEND_3 = 9

    """
    You will implement this class for the competition.
    You can add any additional variables / methods in this file. 
    Do not modify the class name or the base class and do not modify the lines marked below.
    """

    #Some superclass player data includes:
    #self.dict_moves
    #self.player_num = id
    #self.max_units
    #self.nodes
    #self.board
    #self.list_graph
    def __init__(self, p_id):
        super().__init__(p_id)  #Initializes the super class. Do not modify!

        #Our player specific data

        #Updated to store current nodes that are "on the edge"
        self.edgeList = []
        #Updated to store current nodes that are bordering our edge
        self.neighborList = []

        #Priority queue to store our enumerated types, default in above
        self.prioritiesPQ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        return


    #This function gets the neighbors of the given node that are owned by self
    def get_friendly_neighbors(self, node):
        neighbors = self.board.neighbors(node)
        owned_neighbors = []

        for n in neighbors:
            n_node = self.board.nodes[n]
            if(n_node['owner'] == self.player_num) owned_neighbors.append(n_node)

        return owned_neighbors

    #This function gets the neighbors of the given node that are neutral
    def get_neutral_neighbors(self, node):
        neighbors = self.board.neighbors(node)
        neutral_neighbors = []
        
        for n in neighbors:
            n_node = self.board.nodes[n]
            if(n_node['owner'] == None) neutral_neighbors.append(n_node)

        return neutral_neighbors

    #This function gets the neighbors of the given node that are enemies
    def get_enemy_neighbors(self, node):
        neighbors = self.board.neighbors(node)
        enemy_neighbors = []

        for n in neighbors:
            n_node = self.board.nodes[n]
            if(n_node['owner'] != None and n_node['owner'] != self.player_num):
                owned_neighbors.append(n_node)

        return enemy_neighbors

    #This function gets all neighbor nodes that are neutral
    #Call after get_edge_nodes, pass in the lists for better processing
    def get_all_neutral_neighbors(edgeNodes):
        neutral_neighbors = set([])

        our_nodes = self.board.nodes
        
        for node in our_nodes:
            if(node['owner'] == self.player_num):
               n_neutral_neighbors = get_neutral_neighbors(self, node)
               for neighbor in n_neutral_neighbors:
                   neutral_neighbors.add(neighbor)

        return list(neutral_neighbors)

    #This function gets all neighbor nodes that are enemies
    #Call after get_edge_nodes, pass in the lists for better processing
    def get_all_enemy_neighbors(edgeNodes):
        enemy_neighbors = set([])

        our_nodes = self.board.nodes
        
        for node in our_nodes:
            if(node['owner'] == self.player_num):
                n_enemy_neighbors = get_enemy_neighbors(self, node)
                for neighbor in n_enemy_neighbors:
                    enemy_neighbors.add(neighbor)

        return list(enemy_neighbors)

    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables

        """
        Insert any player-specific turn initialization code here
        """
        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        """
        Insert player logic here to determine where to place your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
