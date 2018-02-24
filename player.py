from base_player import BasePlayer
import math
import networkx as nx

class Player(BasePlayer):

    #Substitute for enum
    #Each type is an integer
    SPREAD = 0
    ATTACK_1 = 1
    ATTACK_2 = 2
    ATTACK_3 = 3

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
        self.edge_list = []
        #Updated to store current nodes that are bordering our edge
        self.neighbor_list = []

        #Priority queue to store our enumerated types, default in above
        self.prioritiesPQ = []
        #APT is stored by ID. Our own player ID may not align with the first index of this list
        self.aptList = [5, 5, 5, 5]
        #Keeps track of previous interior nodes to see if we have gained or
        #lost ground against the enemy
        self.previous_interior = []
        #Keeps track of previous edge nodes to see if we have gained or
        #lost ground against the enemy
        self.previous_edge = []
        return

    #This function returns all of our nodes
    def get_our_nodes(self):
        all_nodes = self.board.nodes
        our_nodes = []
        for n in all_nodes:
            if(n['owner'] == self.player_num): our_nodes.append(n)

        return our_nodes

    #This function gets the neighbors of the given node that are owned by self
    def get_friendly_neighbors(self, node):
        neighbors = self.board.neighbors(node)
        owned_neighbors = []

        for n in neighbors:
            n_node = self.board.nodes[n]
            if(n_node['owner'] == self.player_num): owned_neighbors.append(n_node)

        return owned_neighbors

    #This function gets the neighbors of the given node that are neutral
    def get_unfriendly_neighbors(self, node):
        neighbors = self.board.neighbors(node)
        unfriendly_neighbors = []
        
        for n in neighbors:
            n_node = self.board.nodes[n]
            if(n_node['owner'] != self.player_num): unfriendly_neighbors.append(n_node)

        return unfriendly_neighbors

    #This function gets all neighbor nodes that are enemies
    def update_list_info(self):
        neighbor_set = set(self.neighbor_list)
        edge_set = set(self.edge_list)

        our_nodes = get_our_nodes(self)
        
        for node in our_nodes:
            n_unfriendly_neighbors = get_unfriendly_neighbors(self, node)
            num_neighbors = 0
            for neighbor in n_unfriendly_neighbors:
                neighbor_set.add(neighbor)
                num_neighbors += 1
            if(num_neighbors > 0): edge_set.add(node)

        self.edge_list = list(edge_set)
        self.neighbor_list = list(neighbor_set)

    #Calculates the apt for the board and given player ID
    def calc_apt(board, p_id):
        nodes = self.board.nodes
        counter = 0

        for node in nodes:
            if (node['owner'] == p_id):
                counter += 1

        return 4 + math.floor((1 - pow(.9, counter)) / (1 - .9))
    
    def update_apt_list(self, board):
        self.aptList[0] = calc_apt(board, 'p1')
        self.aptList[1] = calc_apt(board, 'p2')
        self.aptList[2] = calc_apt(board, 'p3')
        self.aptList[3] = calc_apt(board, 'p4')

        return
    
    #Update self.previous_interior; run at end of turn before
    #update_previous_edge
    def update_previous_interior(self):
        self.previous_interior = []
        for n in get_our_nodes(self):
            if(self.edge_list.count(n) == 0):
                self.previous_interior.append(n)
        return
        
    #Update self.previous_edge; run at end of turn before updating
    #edge_list and neighbor_list for the next turn
    def update_previous_edge(self):
        self.previous_edge = self.edge_list
        return

    #Orders self.priorityPQ to decide which strategies to implement
    def order_priorities(self):
        self.priorityPQ = []
        heappush(self.prioritiesPQ, (100, SPREAD))
        return

    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables

        #Update self data
        self.edge_list = update_list_data(self, board)
        update_apt_list(self, board)

        
        return


    #Sorts a list of nodes, from lowest to highest, by the army count
    def sort_by_count(nodes):
        for i in range[0, len(nodes)]:
            lowestArmy = 99999999
            for j in range[i, len(nodes)]:
                if nodes[j]['old_units'] < lowestArmy:
                    lowestArmy = nodes[j]['old_units']
                    tempNode = nodes[i]
                    nodes[i] = nodes[j]
                    nodes[j] = tempNode

        return nodes

    #Returns a node list list. Each list contains the nodes that
    # neighbor the corresponding neighbor node in self.neighbor_list
    def get_adjacent_own_nodes(self):
        n_list = [[]]

        for n in self.neighbor_list:
            n_list.append([get_friendly_neighbors(self, n)])

        return n_list

            
    #Creates a spread-type placeset
    #Returns a list of (node, amount)
    def create_spread_place(self, units_to_place):

        place_list = []
        #Prioritize low-army territories in adjacency
        self.neighbor_list = sort_by_count(self.neighbor_list)
        own_adjacency_list = get_adjacent_own_nodes(self)

        units_left = units_to_place

        #Find best places to put armies
        for i in range[0, len(own_adjacency_list)]:
            node_list = sort_by_count(own_adjacency_list[i])
            best_node = node_list[len(node_list) - 1]
            if self.neighbor_list[i]['old_units'] - best_node['old_units'] < units_left:
                place_list.append[(best_node, self.neighbor_list[i]['old_units'] - best_node['old_units'] + 1)]
                units_left = units_left - (self.neighbor_list[i]['old_units'] - best_node['old_units'] + 1)

        return place_list


    def create_attack_place(self, units_to_place, p_id):
        return None

    #This pops the top priority off the heap, calls the correct function
    #Then returns the list of moves corresponding to that type of order
    def enactPriority(self, units_to_place):
        #Note: the heap will never be empty
        order = heapq.heappop(self.prioritiesPQ)

        list_of_places = []

        #SPREAD
        if order == 0:
            list_of_places = create_spread_place(self, units_to_place)
        #ATTACK
        elif order >= 1 and order <= 3:
            list_of_places = create_attack_place(self, units_to_place, p_id)

        return list_of_places

    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        
        #Add moves here
        units_to_place = self.max_units
        while units_to_place > 0:
            #new_place_order is of (node * int) list
            new_place_order_list = enactPriority(self, units_to_place)
            #Subtract the armies used
            for order in new_place_order_list:
                units_to_place -= new_place_order[1]
            super().place_unit(self, new_place_order[0], new_place_order[1])
            

        return self.dict_moves #Returns moves built up over the phase. Do not modify!



    def create_spread_move(self, units_to_place):
        move_list = []
        #Prioritize low-army territories in adjacency
        self.neighbor_list = sort_by_count(self.neighbor_list)
        own_adjacency_list = get_adjacent_own_nodes(self)

        #Attack with the ones that have more armies on it
        for i in range[0, len(own_adjacency_list)]:
            node_list = sort_by_count(own_adjacency_list[i])
            best_node = node_list[len(node_list) - 1]
            #Take the node with the highest number of armies
            if best_node['old_units'] > self.neighbor_list[i]:
                super().move_unit(self, best_node, self.neighbor_list[i], best_node['old_units'] - 1)
        return

    def create_attack_move(self, units_to_place, p_id):
        return

    def enactMovePriority(self):
        #Note: the heap will never be empty
        order = heapq.heappop(self.prioritiesPQ)

        list_of_places = []

        #SPREAD
        if order == 0:
            list_of_places = create_spread_place(self, units_to_place)
        #ATTACK
        elif order >= 1 and order <= 3:
            list_of_places = create_attack_place(self, units_to_place, p_id)

        return

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        
        while units_to_place > 0:
            #new_place_order is of (node * int) list
            new_place_order = enactPriority(self, units_to_place)
            #Subtract the armies used 
            units_to_place -= new_place_order[1]
            super().place_unit(self, new_place_order[0], new_place_order[1])
            

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
