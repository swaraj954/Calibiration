from Full_network_structure import *
import os
import matplotlib
import warnings

warnings.filterwarnings(
    "ignore",
    message="FigureCanvasAgg is non-interactive"
)
matplotlib.use("Agg")

FLOW_TOLERANCE = 10**(-5)

os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
os.makedirs("weird_shapes", exist_ok=True)
# wn=build_full_water_network()
# print("Built water network successfully....")
# close_all_pipes(wn=wn, excluded_pipes=["M1","M2","M3","P1","P6","P7","P8"])

#rectangle with one finger extended(No pipe with zero flow)
def weird_shape_sim_1(wn:wntr.network.WaterNetworkModel):
    #os.chdir("weird_shapes")
    #os.mkdir("ws1")
    #os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    open_pipes(wn,["-IJ1","IJ1-IJ2","IJ4-IJ2","P2","-IJ3","IJ3-IJ4","IJ2-"])
    wntr.network.write_inpfile(wn=wn,filename="weird_shapes/ws1/wn.inp")
    fig,ax = plot_open_pipes("weird_shapes/ws1/wn.inp")
    plt.show()
    fig.savefig("weird_shapes/ws1/open_pipes_plot.png", dpi=300)
    wn.options.time.duration =24*3600
    wn.options.time.report_timestep=3600
    wn.options.time.hydraulic_timestep=60
    sim = wntr.sim.EpanetSimulator(wn=wn)
    print("Running Simulation....")
    results = sim.run_sim()
    print("\nDone.")
    flows = results.link["flowrate"]
    wntr.graphics.plot_network(wn=wn,link_attribute=flows.iloc[4],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
    figg = plt.gcf()
    axx = plt.gca()
    figg.savefig("weird_shapes/ws1/pipe_flows.png")
    plt.show()
    flows.to_csv("weird_shapes/ws1/pipe_flows.csv")
    results.link["status"].to_csv("weird_shapes/ws1/pipe_status.csv")

#2 squares sharing a corner(No pipe with 0 flow)
def weird_shape_sim_2(wn:wntr.network.WaterNetworkModel):
    # os.chdir("weird_shapes")
    # os.mkdir("ws2")
    # os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    open_pipes(wn,["-IJ1","IJ1-IJ2","IJ4-IJ2","P2","-IJ3","IJ3-IJ4","IJ4-","IJ4-IJ6","IJ6-","P4_2","P4_3"])
    wntr.network.write_inpfile(wn=wn,filename="weird_shapes/ws2/wn.inp")
    fig,ax = plot_open_pipes("weird_shapes/ws2/wn.inp")
    plt.show()
    fig.savefig("weird_shapes/ws2/open_pipes_plot.png", dpi=300)
    wn.options.time.duration =24*3600
    wn.options.time.report_timestep=3600
    wn.options.time.hydraulic_timestep=60
    sim = wntr.sim.EpanetSimulator(wn=wn)
    print("Running Simulation....")
    results = sim.run_sim()
    print("\nDone.")
    flows = results.link["flowrate"]
    wntr.graphics.plot_network(wn=wn,link_attribute=flows.iloc[4],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
    figg = plt.gcf()
    axx = plt.gca()
    figg.savefig("weird_shapes/ws2/pipe_flows.png")
    plt.show()
    flows.to_csv("weird_shapes/ws2/pipe_flows.csv")
    results.link["status"].to_csv("weird_shapes/ws2/pipe_status.csv")


#Dangling dead end pipe
def weird_shape_sim_3(wn:wntr.network.WaterNetworkModel):
    # os.chdir("weird_shapes")
    # os.mkdir("ws3")
    # os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    open_pipes(wn,["P2","-IJ1","IJ1-IJ2","IJ2-"])
    wntr.network.write_inpfile(wn=wn,filename="weird_shapes/ws3/wn.inp")
    fig,ax = plot_open_pipes("weird_shapes/ws3/wn.inp")
    plt.show()
    fig.savefig("weird_shapes/ws3/open_pipes_plot.png", dpi=300)
    wn.options.time.duration =24*3600
    wn.options.time.report_timestep=3600
    wn.options.time.hydraulic_timestep=60
    sim = wntr.sim.EpanetSimulator(wn=wn)
    print("Running Simulation....")
    results = sim.run_sim()
    print("\nDone.")
    flows = results.link["flowrate"]
    wntr.graphics.plot_network(wn=wn,link_attribute=flows.iloc[4],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
    figg = plt.gcf()
    axx = plt.gca()
    figg.savefig("weird_shapes/ws3/pipe_flows.png")
    plt.show()
    flows.to_csv("weird_shapes/ws3/pipe_flows.csv")
    results.link["status"].to_csv("weird_shapes/ws3/pipe_status.csv")



#one pipe open inside an almost symmetric layout(No pipe with zero flow)
def weird_shape_sim_4(wn:wntr.network.WaterNetworkModel):
    # os.chdir("weird_shapes")
    # os.mkdir("ws4")
    # os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    open_pipes(wn,["-IJ1","IJ1-IJ2","IJ4-IJ2","P2","-IJ3","IJ3-IJ4","IJ2-","IJ1-IJ3"])
    wntr.network.write_inpfile(wn=wn,filename="weird_shapes/ws4/wn.inp")
    fig,ax = plot_open_pipes("weird_shapes/ws4/wn.inp")
    plt.show()
    fig.savefig("weird_shapes/ws4/open_pipes_plot.png", dpi=300)
    wn.options.time.duration =24*3600
    wn.options.time.report_timestep=3600
    wn.options.time.hydraulic_timestep=60
    sim = wntr.sim.EpanetSimulator(wn=wn)
    print("Running Simulation....")
    results = sim.run_sim()
    print("\nDone.")
    flows = results.link["flowrate"]
    wntr.graphics.plot_network(wn=wn,link_attribute=flows.iloc[4],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
    figg = plt.gcf()
    axx = plt.gca()
    figg.savefig("weird_shapes/ws4/pipe_flows.png")
    plt.show()
    flows.to_csv("weird_shapes/ws4/pipe_flows.csv")
    results.link["status"].to_csv("weird_shapes/ws4/pipe_status.csv")




def weird_shape_sim_5(wn:wntr.network.WaterNetworkModel):
    os.chdir("weird_shapes")
    os.mkdir("ws5")
    os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    open_pipes(wn,["-IJ1","IJ1-IJ2","P2","-IJ3","IJ3-IJ4","IJ2-","IJ1-IJ3","IJ4-","P4_3"])
    wntr.network.write_inpfile(wn=wn,filename="weird_shapes/ws5/wn.inp")
    fig,ax = plot_open_pipes("weird_shapes/ws5/wn.inp")
    plt.show()
    fig.savefig("weird_shapes/ws5/open_pipes_plot.png", dpi=300)
    wn.options.time.duration =24*3600
    wn.options.time.report_timestep=3600
    wn.options.time.hydraulic_timestep=60
    sim = wntr.sim.EpanetSimulator(wn=wn)
    print("Running Simulation....")
    results = sim.run_sim()
    print("\nDone.")
    flows = results.link["flowrate"]
    wntr.graphics.plot_network(wn=wn,link_attribute=flows.iloc[4],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
    figg = plt.gcf()
    axx = plt.gca()
    figg.savefig("weird_shapes/ws5/pipe_flows.png")
    plt.show()
    flows.to_csv("weird_shapes/ws5/pipe_flows.csv")
    results.link["status"].to_csv("weird_shapes/ws5/pipe_status.csv")

    

def weird_shape_hit_and_trial():
    wn = build_full_water_network()
    valid_path = make_shape_random_walk(wn)
    if valid_path:
        open_non_grid_pipes(wn)
        # fig,ax =plot_open_pipess(wn)
        # plt.show()

        pipes_to_observe = []
        for pipe in wn.link_name_list:
            actual_pipe:wntr.network.Pipe = wn.get_link(pipe)
            if actual_pipe.initial_status==wntr.network.LinkStatus.Open:
                pipes_to_observe.append(pipe)
        
        #print(pipes_to_observe)
        wn.options.time.duration =24*3600
        wn.options.time.report_timestep=3600
        wn.options.time.hydraulic_timestep=60
        simulator = wntr.sim.EpanetSimulator(wn=wn)
        results = simulator.run_sim()

        flows_of_interest = results.link["flowrate"].iloc[-1]
        flows_of_interest = flows_of_interest.loc[pipes_to_observe]
        flow_list = flows_of_interest.tolist()
        
        for each_value in flow_list:
            if abs(each_value) < FLOW_TOLERANCE:
                return (True,wn,results,pipes_to_observe)

        return (False,wn,results,pipes_to_observe)
    else:
        results=[]
        return (False,wn,results,["null"])



def find_weird_shapes(iterations:int,i:int = 6):
    iter = 0
    intial_i=i
    while True:
        
        (flag,network,results,open_pipes) = weird_shape_hit_and_trial()
        if flag and iter<iterations:
           
            os.chdir("weird_shapes")
            if not os.path.isdir(f"ws{i}"):
                os.makedirs(f"ws{i}")
            os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")

            wntr.network.write_inpfile(wn=network,filename=f"weird_shapes/ws{i}/wn.inp")

            fig,ax = plot_open_pipes(f"weird_shapes/ws{i}/wn.inp")
            
            fig.savefig(f"weird_shapes/ws{i}/open_pipes_plot.png", dpi=300)
            plt.close(fig)
            #plt.show()
            flows = results.link["flowrate"]
            wntr.graphics.plot_network(wn=network,link_attribute=flows.iloc[-1],title="FLows",link_width=2,node_size=30,link_cmap=plt.cm.viridis)
            figg = plt.gcf()
            axx = plt.gca()
            figg.savefig(f"weird_shapes/ws{i}/pipe_flows.png")
            plt.close(figg)
            #plt.show()
            flows.to_csv(f"weird_shapes/ws{i}/pipe_flows.csv")
            results.link["status"].to_csv(f"weird_shapes/ws{i}/pipe_status.csv")

            with open(f"weird_shapes/ws{i}/open_pipes.txt", "w") as f:
                for item in open_pipes:
                    f.write(f"{item}\n") 

            i=i+1
            print(f"Total Weird shapes found so far:{i-intial_i}")
        elif iter==iterations:
            break
        else:
            #print("SHAPE NOT WIERD:(")
            pass
        print(f"--------------------\nON Iteration:{iter}")
        print("Open figures:", len(plt.get_fignums()))
        print("------------------------------------------")
        if(len(plt.get_fignums())>1):
            plt.close("all")
        iter=iter+1
        
        
    
        
            

find_weird_shapes(3000,1)




   
    
    

#weird_shape_sim_5(wn=wn)
