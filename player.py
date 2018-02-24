from base_player import BasePlayer
import math
import networkx as nx

class Player(BasePlayer):

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
        #Of type int list
        self.edge_list = []
        #Updated to store current nodes that are bordering our edge
        #Of type int list
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
    #Input: self
    #Returns an int list
    def get_our_nodes(self):
        all_nodes = self.board.nodes
        our_nodes = []
        for i in range[0, len(all_nodes)]:
            if(all_nodes[i]['owner'] == self.player_num): our_nodes.append(i)

        return our_nodes

    #This function gets the neighbors of the given node that are owned by self
    #Input: self, int
    #Returns an int list
    def get_friendly_neighbors(self, node):
        #Int list
        neighbors = self.board.neighbors(node)
        owned_neighbors = []

        for n in neighbors:
            if (self.board.nodes[n]['owner'] == self.player_num):
                owned_neighbors.append(n)

        return owned_neighbors

    #This function gets the neighbors of the given node that are neutral
    #Input: self, int
    def get_unfriendly_neighbors(self, node):
        #Int list
        neighbors = self.board.neighbors(node)
        neutral_neighbors = []

        for n in neighbors:
            if (self.board.nodes[n]['owner'] == None):
                neutral_neighbors.append(n)

        return neutral_neighbors

    #This function gets all neighbor nodes that are enemies
    #Input: self
    #No output
    def update_list_info(self):
        neighbor_set = set(self.neighbor_list)
        edge_set = set(self.edge_list)

        our_nodes = get_our_nodes(self)
        
        for node in our_nodes:
            n_unfriendly_neighbors = self.get_unfriendly_neighbors(self, node)
            num_neighbors = 0
            for neighbor in n_unfriendly_neighbors:
                neighbor_set.add(neighbor)
                num_neighbors += 1
            if (num_neighbors > 0): edge_set.add(node)

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
        self.aptList[0] = self.calc_apt(board, 'p1')
        self.aptList[1] = self.calc_apt(board, 'p2')
        self.aptList[2] = self.calc_apt(board, 'p3')
        self.aptList[3] = self.calc_apt(board, 'p4')

        return
    
    #Update self.previous_interior; run at end of turn before
    #update_previous_edge
    def update_previous_interior(self):
        self.previous_interior = []
        for n in self.get_our_nodes(self):
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
        self.update_list_info(self)
        self.update_apt_list(self, board)
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
            n_list.append([self.get_friendly_neighbors(self, n)])

        return n_list

    #Creates a spread-type placeset
    #Returns a list of (node, amount)
    def create_spread_place(self, units_to_place):

        place_list = []
        #Prioritize low-army territories in adjacency
        self.neighbor_list = self.sort_by_count(self.neighbor_list)
        own_adjacency_list = self.get_adjacent_own_nodes(self)

        for node_list in own_adjacency_list:
            node_list = self.sort_by_count(node_list)
            best_node = node_list[len(node_list) - 1]
        return

    def create_attack_place(self, units_to_place, p_id):
        #Figure out what nodes we need to place
        adjacent_nodes = []
        for n in self.edge_list:
            n_neighbors = self.get_unfriendly_neighbors(self, n)
            for neighbor in n_neighbors:
                if (neighbor['owner'] == p_id): 
                    adjacent_nodes.append(neighbor)
                    break

        #Make a list that keeps track of how much the enemy had last time
        adjacent_to_p = []
        total_armies = 0
        for n in adjacent_nodes:
            num_armies = 0
            for neighbor in self.get_unfriendly_neighbors(self, n):
                num_armies += neighbor['old_units']
            adjacent_to_p.append((n, num_armies))
            total_armies += num_armies

        ratio = units_to_place / total_armies

        #We approportion the armies based on how much better we think we're doing
        #If units_to_place is 2x total_armies, we approprotion proportionately
        #Else, we choose one place randomly to attack in force
        placement_orders = []
        if (ratio > 2.0):
            for n in adjacent_to_p:
                placement_orders.append((n[0], int(n[1]*ratio)))
        else:
            node_id = random.randint(0, placement_orders.length - 1)
            placement_orders = [(adjacent_to_p[node_id], units_to_place)]

        return placement_orders


    #This pops the top priority off the heap, calls the correct function
    #Then returns the list of moves corresponding to that type of order
    def enactPriority(self, units_to_place):
        #Note: the heap will never be empty
        order = heapq.heappop(self.prioritiesPQ)

        list_of_places = []

        #SPREAD
        if order == 0:
            list_of_places = self.create_spread_place(self, units_to_place)
        #ATTACK
        elif order >= 1 and order <= 3:
            list_of_places = self.create_attack_place(self, units_to_place, p_id)

        return list_of_places

    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        
        place_list_temp = []
        place_list_final = []
        armies_left = self.max_units
        
        if ('p1' != self.player_num):
            place_list_temp.append(self.create_attack_place(self, armies_left, 'p1'))
        if ('p2' != self.player_num):
            place_list_temp.append(self.create_attack_place(self, armies_left, 'p2'))
        if ('p3' != self.player_num):
            place_list_temp.append(self.create_attack_place(self, armies_left, 'p3'))
        if ('p4' != self.player_num):
            place_list_temp.append(self.create_attack_place(self, armies_left, 'p4'))

        for place in place_list_temp:
            #Make sure the move doesn't result in negative armies placed
            if armies_left - place[1] > 0:
                armies_left = armies_left - place[1]
                place_list_final.append[place]

        #Submit the move
        for place in place_list_final:
            super().place_unit(self, place[0], place[1])

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def filter_by_id(self, nodes, p_id):
        result_list = []

        for node in nodes:
            if self.board.nodes[node]['owner'] == p_id:
                result_list.append[node]

        return result_list
    
    def player_move_units(self):
    
        #Creates a list of all adjacent enemies
        enemy_neighbor_list = []
        if ('p1' != self.player_num):
            enemy_neighbor_list.append(self.filter_by_id(self.neighbor_list, 'p1'))
        if ('p2' != self.player_num):
            enemy_neighbor_list.append(self.filter_by_id(self.neighbor_list, 'p2'))
        if ('p3' != self.player_num):
            enemy_neighbor_list.append(self.filter_by_id(self.neighbor_list, 'p3'))
        if ('p4' != self.player_num):
            enemy_neighbor_list.append(self.filter_by_id(self.neighbor_list, 'p4'))

        #Creates a list of all adjacent neutrals
        neutral_neighbor_list = self.filter_by_id(self.neighbor_list, None)

        #Sorts the enemies by count (least to greatest)
        enemy_neighbor_list = self.sort_by_count(enemy_neighbor_list)
        #Sorts the neutrals by count (least to greatest)
        neutral_neighbor_list = self.sort_by_count(neutral_neighbor_list)

        #Gives our nodes that touch the sorted enemies (in tuples)
        our_neighbor_enemy_list = self.get_adjacent_own_nodes(enemy_neighbor_list)
        #Gives our nodes that touch the sorted neutrals (in tuples)
        our_neighbor_neutral_list = self.get_adjacent_own_nodes(neutral_neighbor_list)


        for i in range[0, len(our_neighbor_enemy_list)]:
            node_list = self.sort_by_count(our_neighbor_enemy_list[i])
            best_node = node_list[len(node_list) - 1]
            if enemy_neighbor_list[i]['old_units'] - best_node['old_units'] < units_left:
                super().move_unit(self, best_node, enemy_neighbor_list[i], best_node['old_units'] - 1)

        for i in range[0, len(our_neighbor_neutral_list)]:
            node_list = self.sort_by_count(our_neighbor_neutral_list[i])
            best_node = node_list[len(node_list) - 1]
            if nuetral_neighbor_list[i]['old_units'] - best_node['old_units'] < units_left:
                super().move_unit(self, best_node, neutral_neighbor_list[i], best_node['old_units'] - 1)                    

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
