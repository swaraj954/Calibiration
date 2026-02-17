from outer_perimeter_structure_replica import *
import wntr
import random
import networkx as nx
import matplotlib.pyplot as plt
import random
from wntr.network import LinkStatus



def build_full_water_network():

    #os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    

    #add junctions
    outer_struc = build_water_network()
    outer_struc.add_junction("InnerJ1",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(3,15))
    outer_struc.add_junction("InnerJ2",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(10,15))
    outer_struc.add_junction("InnerJ3",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(4,12))
    outer_struc.add_junction("InnerJ4",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(9,11))
    outer_struc.add_junction("InnerJ5",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(2,11))
    outer_struc.add_junction("InnerJ6",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(8,9))
    outer_struc.add_junction("InnerJ7",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(2,8))
    outer_struc.add_junction("InnerJ8",elevation=DEFAULT_PIPE_ELEVATION,coordinates=(11,3))

    #add horizontal pipes
    #----------------------------------------------------------
    outer_struc.add_pipe("IJ1-IJ2","InnerJ1","InnerJ2")
    outer_struc.add_pipe("-IJ1","J5","InnerJ1")
    outer_struc.add_pipe("IJ2-","InnerJ2","J8")
    outer_struc.remove_link("P5")
    #----------------------------------------------------------
    outer_struc.add_pipe("IJ3-IJ4","InnerJ3","InnerJ4")
    outer_struc.add_pipe("-IJ3","J5_1","InnerJ3")
    outer_struc.add_pipe("IJ4-","InnerJ4","J7_3")
    #-----------------------------------------------------------
    outer_struc.add_pipe("IJ5-IJ6","InnerJ5","InnerJ6")
    outer_struc.add_pipe("-IJ5","J5_2","InnerJ5")
    outer_struc.add_pipe("IJ6-","InnerJ6","J7_2")
    #-----------------------------------------------------------
    outer_struc.add_pipe("IJ7-IJ8","InnerJ7","InnerJ8")
    outer_struc.add_pipe("-IJ7","J5_3","InnerJ7")
    outer_struc.add_pipe("IJ8-","InnerJ8","J7_1")
    #-----------------------------------------------------------

    #add vertical pipes

    outer_struc.add_pipe("IJ1-IJ3","InnerJ1","InnerJ3")
    outer_struc.add_pipe("IJ2-IJ4","InnerJ2","InnerJ4")

    outer_struc.add_pipe("IJ3-IJ5","InnerJ3","InnerJ5")
    outer_struc.add_pipe("IJ5-IJ7","InnerJ5","InnerJ7")
    outer_struc.add_pipe("IJ7-IJ61","InnerJ7","J6_1")


    outer_struc.add_pipe("IJ4-IJ6","InnerJ4","InnerJ6")
    outer_struc.add_pipe("IJ6-IJ8","InnerJ6","InnerJ8")
    outer_struc.add_pipe("IJ8-IJ61","InnerJ8","J6_2")

    wntr.network.write_inpfile(outer_struc,"Full_Structure.inp")

    return outer_struc



def make_shape(full_model:wntr.network.WaterNetworkModel,open_probability = 0.5):
    start_node = "J5"
    end_node   = "J8"
    excluded_pipes=["M1","M2","M3","P8","P7","P1","P6"]

    for pipe in full_model.pipe_name_list:
        if not pipe in excluded_pipes:
            if random.random()<=open_probability:
                #print(f"Opened this one:{pipe}")
                actual_pipe:wntr.network.Pipe= full_model.get_link(pipe)
                actual_pipe.initial_status = wntr.network.LinkStatus.Open
            else:
                #print(f"CLOSED this one:{pipe}")
                actual_pipe:wntr.network.Pipe= full_model.get_link(pipe)
                actual_pipe.initial_status = wntr.network.LinkStatus.Closed
        else:
            actual_pipe:wntr.network.Pipe= full_model.get_link(pipe)
            actual_pipe.initial_status = wntr.network.LinkStatus.Closed

    model_graph = full_model.to_graph()

    for every_pipe in full_model.pipe_name_list:
        actual_pipe:wntr.network.Pipe = full_model.get_link(every_pipe)
        if actual_pipe.initial_status == wntr.network.LinkStatus.Closed:
            sn = actual_pipe.start_node_name
            en = actual_pipe.end_node_name
            model_graph.remove_edge(sn,en)
        


        

    return_value=False

    if nx.has_path(model_graph,start_node,end_node):
        return_value=True
    else:
        return_value=False

    for pipe in excluded_pipes:
        actual_pipe:wntr.network.Pipe= full_model.get_link(pipe)
        actual_pipe.initial_status = wntr.network.LinkStatus.Open

    return return_value

#AI generated
def get_adjacency(wn):
    adjacency = {node: [] for node in wn.node_name_list}

    for pipe_name in wn.pipe_name_list:
        pipe = wn.get_link(pipe_name)
        u = pipe.start_node_name
        v = pipe.end_node_name

        adjacency[u].append((v, pipe_name))
        adjacency[v].append((u, pipe_name))

    return adjacency


#Ai generated
def random_walk_path(wn, start_node, end_node):

    adjacency = get_adjacency(wn)

    visited = set()
    stack = [(start_node, [])]  # (current_node, path_pipes)

    while stack:
        current, path = stack.pop()

        if current == end_node:
            return path  # list of pipe names

        if current in visited:
            continue

        visited.add(current)

        neighbors = adjacency[current][:]
        random.shuffle(neighbors)

        for neighbor, pipe_name in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [pipe_name]))

    return None  # no path found (shouldn't happen in grid)



def prune_non_path_pipes(wn, start_node, end_node):

    # 1️⃣ Build graph of OPEN pipes
    G = nx.Graph()

    for node in wn.node_name_list:
        G.add_node(node)

    for pipe_name in wn.pipe_name_list:
        pipe = wn.get_link(pipe_name)
        if pipe.initial_status == LinkStatus.OPEN:
            G.add_edge(pipe.start_node_name, pipe.end_node_name)

    # 2️⃣ Nodes reachable from start
    reachable_from_start = nx.node_connected_component(G, start_node)

    # 3️⃣ Nodes reachable from end
    reachable_from_end = nx.node_connected_component(G, end_node)

    # 4️⃣ Only keep nodes that are in BOTH
    valid_nodes = reachable_from_start.intersection(reachable_from_end)

    # 5️⃣ Close pipes that touch invalid nodes
    for pipe_name in wn.pipe_name_list:
        pipe = wn.get_link(pipe_name)

        if pipe.initial_status == LinkStatus.OPEN:
            if (pipe.start_node_name not in valid_nodes or
                pipe.end_node_name not in valid_nodes):
                pipe.initial_status = LinkStatus.CLOSED



def open_non_grid_pipes(full_network:wntr.network.WaterNetworkModel):
    excluded_pipes=["M1","M2","M3","P8","P7","P1","P6"]
    for pipes in excluded_pipes:
        pipe:wntr.network.Pipe = full_network.get_link(pipes)
        pipe.initial_status = LinkStatus.OPEN
        





#Ai generated
def make_shape_random_walk(full_model):

    start_node = "J5"
    end_node   = "J8"

    # 1️⃣ Close all pipes first
    for pipe_name in full_model.pipe_name_list:
        full_model.get_link(pipe_name).initial_status = LinkStatus.CLOSED

    # 2️⃣ Generate random backbone path
    backbone_pipes = random_walk_path(full_model, start_node, end_node)

    if backbone_pipes is None:
        return False

    # 3️⃣ Open backbone pipes
    for pipe_name in backbone_pipes:
        full_model.get_link(pipe_name).initial_status = LinkStatus.OPEN

    # 4️⃣ OPTIONAL: Add random extra pipes for complexity
    for pipe_name in full_model.pipe_name_list:
        if pipe_name not in backbone_pipes:
            if random.random() < 0.3:  # extra complexity factor
                full_model.get_link(pipe_name).initial_status = LinkStatus.OPEN
    
    prune_non_path_pipes(full_model, start_node, end_node)
    open_non_grid_pipes(full_model)
    return True



def reset(full_model:wntr.network.WaterNetworkModel):

    for pipe in full_model.pipe_name_list:
        actual_pipe:wntr.network.Pipe= full_model.get_link(pipe)
        actual_pipe.intial_status = wntr.network.LinkStatus.Open

def close_all_pipes(wn:wntr.network.WaterNetworkModel):
    for pipe in wn.pipe_name_list:
        actual_pipe:wntr.network.Pipe = wn.get_link(pipe)
        actual_pipe.initial_status=wntr.network.LinkStatus.Closed





def plot_open_pipes(inp_file):

    
    wn = wntr.network.WaterNetworkModel(inp_file)

   
    open_pipes = [
        pipe_name
        for pipe_name in wn.pipe_name_list
        if wn.get_link(pipe_name).initial_status == wntr.network.LinkStatus.Open
    ]

   
    plt.figure()
    wntr.graphics.plot_network(wn=wn,link_attribute=open_pipes,node_size=30,link_width=2)
    

    plt.title("Open Pipes Only")
    plt.show()

        
        
def gen_ip_files(number_of_files,open_prob = 0.5):
    i=1
    while i<=number_of_files:
        varied_water_network = build_full_water_network()
        #x = make_shape(varied_water_network,open_prob)
        x=make_shape_random_walk(varied_water_network)
        if x:
            print("TRUE")
            wntr.network.write_inpfile(varied_water_network,f"Shape{i}.inp")
            i=i+1
        else:
            print("FALSEEEE")
        




gen_ip_files(10)
for i in range(1,10):
    plot_open_pipes(f"Shape{i}.inp")


    





    



            
    
        


                



    

os = build_full_water_network()
make_shape(os)











    



    



    


build_full_water_network()

    