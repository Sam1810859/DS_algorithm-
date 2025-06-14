#!/usr/bin/env python3
import sys

# Distance Vector Routing Algorithm Implementation
# here I define functions to implement the distance vector algorithm
def initialise_tables(nodes, routing_table_nodes, links, iteration_count):
    for i in range(len(routing_table_nodes)):
        for j in links:
            link_info = links[j]
            if i == nodes[link_info[0]]:
                routing_table_nodes[i][i][nodes[link_info[1]]] = link_info[2]
                print(f"t={iteration_count} distance from {nodes[i]} to {link_info[1]} via {link_info[1]} is {link_info[2]}")
            if i == nodes[link_info[1]]:
                routing_table_nodes[i][i][nodes[link_info[0]]] = link_info[2]
                print(f"t={iteration_count} distance from {nodes[i]} to {link_info[0]} via {link_info[0]} is {link_info[2]}")
            nodes[f"{link_info[0]}{link_info[1]}"] = link_info[2]
            nodes[f"{link_info[1]}{link_info[0]}"] = link_info[2]
        routing_table_nodes[i][i][i] = 0
    iteration_count += 1
    return routing_table_nodes

# here I define a function to find the minimum cost in a column
def min_column(table, column_no):
    cost_list = []
    for i in range(len(table)):
        if table[i][column_no] is not None:
            cost_list.append(table[i][column_no])
    if (len(cost_list))== 0:
        return None
    return min(cost_list)

# here I am defining a function accepting a value, table, column_no, and node_no to add the value to the routing table
def route_through(value, table, column_no, node_no):
    for i in range(len(table)):
        if node_no != i:
            # check if the value in the specified column matches
            # the value we are looking for
            # if it does, return the index of that row
            # this is to find the next hop in the routing table
            if table[i][column_no] == value:
                return i

# here I define a function to update the routing table until convergence is achieved
def update_table(nodes, routing_table_nodes, iteration_count):
    print(" ") # to add a space before printing the next iteration
    # change_occurred = False
    # this variable is used to track if any changes occur in the routing table
    change_occurred = 0
    for i in range(len(routing_table_nodes)):
        for j in range(len(routing_table_nodes[i])):
            if i != j:
                continue
            for k in range(len(routing_table_nodes[i][j])):
                cost_via_j_to_k = min_column(routing_table_nodes[j],k)
                link_cost_ij = nodes.get(f"{nodes[i]} {nodes[j]}")
                current_cost= routing_table_nodes[i][j][k]

                if k in range(len(routing_table_nodes[i][j])):
                    continue
                new_cost = cost_via_j_to_k + link_cost_ij

                # selfDistance 
                if k == i:
                    if current_cost !=0:
                        routing_table_nodes[i][j][k] = 0 
                        change_occurred = 1
                        continue
                if current_cost != new_cost:
                    routing_table_nodes[i][j][k] = new_cost

                    if min_column(routing_table_nodes[i],j) != new_cost and j !=k:
                        print(f"t={iteration_count} distance from {nodes[i]} to {nodes[k]} via {nodes[j]} is {new_cost}")
                    change_occurred = 1
        return change_occurred, routing_table_nodes
            
# print routing table nodes will be used to display the routing table and accept the nodes, routing table, and iteration count
def print_routing_table_nodes(routing_table_nodes, nodes, iteration_count):
    print(f"\nRouting Table at iteration {iteration_count}:")
    for i in range(len(routing_table_nodes)):
        for j in range(len(routing_table_nodes[i])):
            for k in range(len(routing_table_nodes[i][j])):
                if routing_table_nodes[i][j][k] != float('inf'):
                    print(f"t={iteration_count} distance from {nodes[i]} to {nodes[k]} via {nodes[j]} is {routing_table_nodes[i][j][k]}")
    print("\n#END\n")        

# here implement the process for change config
# # this function will read the change configuration file and update the routing table accordingly
def change_configuration(nodes, routing_table_nodes, change_config_lines, iteration_count):
# implement a counter to track the number of iterations
    iteration_count = 0
    routing_table_nodes = initialise_tables(nodes, routing_table_nodes, links, iteration_count)

    #keep updating the routing table until no changes occur
    while True:
        change_occurred, routing_table_nodes = update_table(nodes, routing_table_nodes, iteration_count)
        if not change_occurred:
            break
        iteration_count += 1    


#parse the configuration file
config_file= open(str(sys.argv[1]), "r")
config_lines = config_file.read().split('\n')
config_file.close()

#parse the change configuration file
change_config_file = open(str(sys.argv[2]), "r")
change_config_lines = change_config_file.read().split('\n')
change_config_file.close()

# read the number of nodes
line_num = 0 
num_nodes = int(config_lines[line_num])
line_num += 1

#dictionary to hold node names and their indices
nodes = {}
for i in range(0, num_nodes):
    nodes[config_lines[line_num + i]] = i
    nodes[i] = config_lines[line_num + i]
print("\n#START\n") 

# read the number of links
line_num += num_nodes
#the number of links between nodes 
num_links = int(config_lines[line_num])
line_num += 1

#dictionary to hold link costs
links = {}
for i in range(0, num_links):
    link_info = config_lines[line_num + i].split()
    links[i] = (nodes[link_info[0]], nodes[link_info[1]], int(link_info[2]))

#initialize the routing table
routing_table_nodes = []
for source_node in range (0, num_nodes):
    routing_table_nodes.append([])
    for vi_neighbor in range(0, num_nodes):
        routing_table_nodes[source_node].append([])
        for destination in range(0, num_nodes):
            routing_table_nodes[source_node].append({"next_hop": None, "cost": float('inf')})


