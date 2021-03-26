import sys

class Btree:
    def __init__(self):
        self.data = None
        self.parent = "None"
        self.distance = 0 
        self.connected_nodes = []
        self.distance_to_nodes = []
        self.route = []
        
# list to keep track of visited nodes
visited_node = []
nodes = []
fringe = {}

src_city = sys.argv[2]
source = sys.argv[2]
des_city = sys.argv[3]
file_name = sys.argv[1]
#file_name = "input1.txt"
fobject = open(file_name,"r")
fdata = fobject.read()
data_By_Comma = []
for row in fdata.split("\n"):
    # print(row)
    data_By_Comma.append(row.split(","))

# print(data_By_Comma)
data_list = list(data_By_Comma)
new_data = []

for row in data_list:
   for entries in row:
        new_data.append(str(entries))
# print(new_data)        
for var_input in new_data:
    inputVar_list = var_input.split(" ")
    #print(inputVar_list)
    
    # if end of input file end the loop processing 
    if inputVar_list[0] == "END" and inputVar_list[1] == "OF" and inputVar_list[2] == "INPUT":
       break
    
    if inputVar_list[0] not in visited_node and inputVar_list[1] not in visited_node:
       # Create root of the tree
       node1 = Btree()
       node1.data = inputVar_list[0]
       visited_node.append(node1.data)
    
       node2 = Btree()
       node2.data = inputVar_list[1]
       node2.connected_nodes.append(node1.data)
       node2.distance_to_nodes.append(inputVar_list[2])
       visited_node.append(node2.data)
       node1.connected_nodes.append(node2.data)
       node1.distance_to_nodes.append(inputVar_list[2])

       nodes.append(node1)
       nodes.append(node2)
    else:
        if inputVar_list[0] not in visited_node and inputVar_list[1] in visited_node:
            node3 = Btree()
            node3.data = inputVar_list[0]
            visited_node.append(node3.data)
            node3.connected_nodes.append(inputVar_list[1])
            node3.distance_to_nodes.append(inputVar_list[2])
            nodes.append(node3)
            node4 = Btree()
            index = 0
            i= 0
            for row in nodes:
                if row.data == inputVar_list[1]:
                   index = i 
                i = i + 1
            node4 = nodes[index]
            node4.connected_nodes.append(node3.data)
            node4.distance_to_nodes.append(inputVar_list[2])
        else:        
            if inputVar_list[0] in visited_node and inputVar_list[1] not in visited_node:
               # print(str(visited_node))
               node5 = Btree()
               node5.data = inputVar_list[1]
               visited_node.append(node5.data)
               node5.connected_nodes.append(inputVar_list[0])
               node5.distance_to_nodes.append(inputVar_list[2])
               nodes.append(node5)
               node6 = Btree()
               index = 0
               i = 0
               for row in nodes:
                   if row.data == inputVar_list[0]:
                      index = i 
                   i = i + 1
               node6 = nodes[index]
               node6.connected_nodes.append(node5.data)
               node6.distance_to_nodes.append(inputVar_list[2])
            else:
                if inputVar_list[0] in visited_node and inputVar_list[1] in visited_node:
                   node7 = Btree()
                   index = 0
                   i= 0
                   for row in nodes:
                       if row.data == inputVar_list[0]:
                          index = i 
                       i = i + 1
                   node7 = nodes[index]
                   node7.connected_nodes.append(inputVar_list[1])
                   node7.distance_to_nodes.append(inputVar_list[2])

                   node8 = Btree()
                   index = 0
                   i= 0
                   for row in nodes:
                       if row.data == inputVar_list[1]:
                          index = i 
                       i = i + 1
                   node8 = nodes[index]
                   node8.connected_nodes.append(node7.data)
                   node8.distance_to_nodes.append(inputVar_list[2])
node_list_string = []
for row in nodes:
    node_list_string.append(row.data)

total_distance = 0
new_visited_list = []
final_route = {}

# add first node to the priority queue
fringe = {src_city:0}
s_flag = 0
d_flag = 0
loop_var = 0
while len(fringe) != 0:
      # check if destination node
      if src_city == des_city: 
         break
      if loop_var == 0:
         if src_city not in node_list_string:
            s_flag = 1 
         if des_city not in node_list_string:
            d_flag = 1
      if s_flag == 1 or d_flag == 1:
         break
      # retrieve current node from nodes
      current_node = Btree()
      i = 0
      index = 0
      for row in nodes:
          if src_city == row.data:
             index = i
          i = i + 1
      current_node = nodes[index]
      # Add all the connected nodes to the priority queue
      i = 0
      index = 0
      
      for row in current_node.connected_nodes:
          # review the line below
          # retrieve the node from node list
          j = 0
          index_j = 0          
          for entry in nodes:
              if row == entry.data:
                 index_j = j
              j = j + 1    
          set_parent_node = Btree()
          set_parent_node = nodes[index_j]
          # check if node present in fringe, if yes then validate and updation if not then directly update
          if row not in new_visited_list:
             if row in fringe: # visited city condition also before this if
                
                newnodedata = int(current_node.distance_to_nodes[i]) + fringe[current_node.data] 
                #print(newnodedata)
                if fringe[row] > newnodedata:
                   fringe[row] = newnodedata
                   set_parent_node.parent = current_node.data
                   set_parent_node.distance = current_node.distance_to_nodes[i]                  
             else: 
                 fringe[row] = int(current_node.distance_to_nodes[i]) + fringe[current_node.data]   
                 set_parent_node.parent = current_node.data
                 set_parent_node.distance = current_node.distance_to_nodes[i]
          i = i + 1
      
      new_visited_list.append(current_node.data) 
      # remove the node from fringe i.e Priority queue
      del fringe[current_node.data]
      # sort priority queue
      sorted_list = []
      sorted_list = sorted(fringe.values())
      for key in fringe:
          if fringe[key] == sorted_list[0]:
             src_city = key
             break
      if src_city in fringe:
         total_distance = fringe[src_city]
      else:
         total_distance = 99999999
      loop_var = loop_var + 1
print("nodes expanded: "+str(loop_var))

# code to generate output
if s_flag == 0 and d_flag == 0:
   if total_distance != 99999999:
      print("distance: "+str(total_distance)+" km")
   else:
      print("distance:"+" infinite")

if s_flag == 1 and d_flag == 1:
   print("Source and Destination city didn't found ")
else:
   if s_flag == 1:
      print("Source city didn't found")
   else:
      if d_flag == 1:
         print("Destination city didn't found")

i = 1
city_route_list = []
for row in nodes:
    j = 0
    index_j = 0
    for entry in nodes:
        if des_city == entry.data:
           index_j = j
           break
        j = j + 1
    city_route = nodes[index_j]
    city_route_list.append(nodes[index_j])
    if city_route == source:
       break
    des_city = city_route.parent
    #print(city_route.distance)

city_route_list_reverse = []
for row in city_route_list:
    if row.parent == "None":
       break
    else:
        city_route_list_reverse.append(row)
        
city_route_list_reverse.reverse()

if s_flag == 0 and d_flag == 0:
   print("Route:")
   i = 0
   # display final output
   if total_distance != 99999999:
      for row in city_route_list_reverse:
          print(source + " to " + row.data + ", " +str(row.distance) + " km")
          source = row.data
   else:
      print("none")


#References: Github, stackoverflow       