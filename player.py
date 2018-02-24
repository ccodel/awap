import BasePlayer

class Player(base_player.BasePlayer):
    def __init__(self, p_id):
        self.dict_moves = {'place': [], 'move': []} # Action dictionary (you should only use our interface to modify this)
        self.player_num = p_id      # each player on a board will have a unique player number
        self.max_units = 0          # max number of units the player can place (updated after calling a place command)
        self.nodes = None           # list of nodes that this player owns (updated every turn)
        self.board = None           # networkx object (updated every turn)
        self.list_graph = None      # list representation of the entire board (updated every turn)

        return


    def init_turn(self, board, nodes, max_units):
        self.dict_moves = {'place': [], 'move': []}
        self.max_units = max_units
        self.nodes = nodes
        self.board = board
        
        return
