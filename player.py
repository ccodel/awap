from base_player import BasePlayer
import networkx as nx

class Player(BasePlayer):

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
        self.edgeList = []
        self.neighborList = []
        return


    #This function gets our own edge nodes
    #Call after board info is updated in self
    def get_edge_nodes(self):

        edgeNodes = []
        
        for node in self.nodes:
            #Get list of neighbors for each of our owned nodes
            neighbors = self.board.neighbors(node)
            for neighbor in neighbors:
                #Iterate through them. If has non-ourself, add to return list
                if self.board.nodes[neighbor]{'owner'} != self.player_num:
                    #Since non-ourself node, add to result list
                    edgeNodes += self.nodes[i]
                    #exit loop to avoid adding edge node too many times
                    j = len(neighbors) + 1

        return edgeNodes
    
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
