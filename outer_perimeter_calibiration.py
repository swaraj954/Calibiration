from outer_perimeter_structure_replica import *
from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args
import numpy as np

os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")

#PIPES_OF_INTEREST = ["M2", "P2_2", "P3_2", "P4_2", "P7"]


MAX_POSSIBLE_FLOW = 10  #Must observe while collecting data, this is just a placeholder value for now

measured_df = pd.read_csv("actual_flows.csv")
#--------------------------------------------------
# Since closed loop network we are asssuming steady 
# state flow after some time and ignoring time
#
# actual_flows.csv's expected format:
# pipe_id,flow
# M2,0.012
# P2_2,0.010
# ...
#
#---------------------------------------------------

#convert measured_df to a dictionary for faster access
MEASURED_FLOWS = dict(zip(measured_df.pipe_id, measured_df.flow))


#convert .yml file into dict
with open("parameter_values.yml") as f:
    mystery_parameters = yaml.safe_load(f)


space = [

    # --- Geometry & tank (±1%) ---
    
    Real(0.99, 1.01, name="DEFAULT_PIPE_ELEVATION_multiplier"),
    Real(0.99, 1.01, name="TANK_TO_PUMP_PIPE_ELEVATION_multiplier"),
    Real(0.99, 1.01, name = "PUMP_TO_FIRST_BEND_PIPE_LENGTH_multiplier"),
    Real(0.99, 1.01, name = "FIRST_BEND_TO_GRID_PIPE_LENGTH_multiplier"),  #error 1 solved here

    Real(0.99, 1.01, name="DEFAULT_PIPE_LENGTH_multiplier"),
    Real(0.99, 1.01, name="TANK_TO_PUMP_PIPE_LENGTH_multiplier"),

    Real(0.99, 1.01, name="BIG_PIPE_DIAMETER_multiplier"),
    Real(0.99, 1.01, name="SMALL_PIPE_DIAMETER_multiplier"),

    Real(0.99, 1.01, name="INITIAL_MAIN_TANK_LEVEL_multiplier"),
    Real(0.99, 1.01, name="MAX_MAIN_TANK_LEVEL_multiplier"),
    Real(0.99, 1.01, name="MAIN_TANK_DIAMETER_multiplier"),

    # --- Pump ---
    Real(5.0, 50.0, name="pump_headloss_a_coeff"),
    Real(100.0, 5000.0, name="pump_headloss_b_coeff"),
]
wnn = build_water_network()
for pipe_id in wnn.pipe_name_list:
    space.append(Real(50.0, 200.0, name=f"roughness_coeff_for_pipe_{pipe_id}"))     #these are now safe names
    space.append(Real(0.00,20.00,name = f"Minor_loss_coeff_for_pipe_{pipe_id}"))


def modify_network_for_this_sim(theta,wn:wntr.network.model):

    DEFAULT_PIPE_ELEVATION_multiplier      = theta["DEFAULT_PIPE_ELEVATION_multiplier"]
    TANK_TO_PUMP_PIPE_ELEVATION_multiplier = theta["TANK_TO_PUMP_PIPE_ELEVATION_multiplier"]
    DEFAULT_PIPE_LENGTH_multiplier         = theta["DEFAULT_PIPE_LENGTH_multiplier"]
    TANK_TO_PUMP_PIPE_LENGTH_multiplier    = theta["TANK_TO_PUMP_PIPE_LENGTH_multiplier"]
    BIG_PIPE_DIAMETER_multiplier           = theta["BIG_PIPE_DIAMETER_multiplier"]
    SMALL_PIPE_DIAMETER_multiplier         = theta["SMALL_PIPE_DIAMETER_multiplier"]
    INITIAL_MAIN_TANK_LEVEL_multiplier     = theta["INITIAL_MAIN_TANK_LEVEL_multiplier"]
    MAX_MAIN_TANK_LEVEL_multiplier         = theta["MAX_MAIN_TANK_LEVEL_multiplier"]
    MAIN_TANK_DIAMETER_multiplier          = theta["MAIN_TANK_DIAMETER_multiplier"]

    PUMP_TO_FIRST_BEND_PIPE_LENGTH_multiplier         = theta["PUMP_TO_FIRST_BEND_PIPE_LENGTH_multiplier"]  #error 2 solved
    FIRST_BEND_TO_GRID_PIPE_LENGTH_multiplier         = theta["FIRST_BEND_TO_GRID_PIPE_LENGTH_multiplier"]

    pump_headloss_a_coeff                  = theta["pump_headloss_a_coeff"]
    pump_headloss_b_coeff                  = theta["pump_headloss_b_coeff"]


    # Vary measured paremters for main tank by +/- 1%
    Main_Tank: wntr.network.Tank = wn.get_node("Main_Tank")
    Main_Tank.diameter  = MAIN_TANK_DIAMETER * MAIN_TANK_DIAMETER_multiplier
    Main_Tank.max_level = MAX_MAIN_TANK_LEVEL* MAX_MAIN_TANK_LEVEL_multiplier
    Main_Tank.init_level= INITIAL_MAIN_TANK_LEVEL * INITIAL_MAIN_TANK_LEVEL_multiplier



    #Vary measured junction elevations by +/- 1%

    junction_list = wn.junction_name_list
    for every_juntion in junction_list:
        if not every_juntion == 'J1':
            current_junction:wntr.network.Junction = wn.get_node(every_juntion)
            current_junction.elevation = DEFAULT_PIPE_ELEVATION * DEFAULT_PIPE_ELEVATION_multiplier
        else:
            current_junction:wntr.network.Junction = wn.get_node(every_juntion)
            current_junction.elevation = TANK_TO_PUMP_PIPE_ELEVATION*TANK_TO_PUMP_PIPE_ELEVATION_multiplier


    
    #Vary Measured pipe params by +/- 1%

    pipe_list = wn.pipe_name_list
    for every_pipe in pipe_list:
        current_pipe:wntr.network.Pipe = wn.get_link(every_pipe)
        if(current_pipe.name=="M1"):
            current_pipe.length = TANK_TO_PUMP_PIPE_LENGTH * TANK_TO_PUMP_PIPE_LENGTH_multiplier
            current_pipe.diameter = BIG_PIPE_DIAMETER * BIG_PIPE_DIAMETER_multiplier
        elif(current_pipe.name=="M2"):
            current_pipe.length = PUMP_TO_FIRST_BEND_PIPE_LENGTH * PUMP_TO_FIRST_BEND_PIPE_LENGTH_multiplier
            current_pipe.diameter = BIG_PIPE_DIAMETER * BIG_PIPE_DIAMETER_multiplier
            
        elif(current_pipe.name=="M3"):
            current_pipe.length    = FIRST_BEND_TO_GRID_PIPE_LENGTH * FIRST_BEND_TO_GRID_PIPE_LENGTH_multiplier
            current_pipe.diameter  = BIG_PIPE_DIAMETER * BIG_PIPE_DIAMETER_multiplier
        else:
            current_pipe.length = DEFAULT_PIPE_LENGTH * DEFAULT_PIPE_LENGTH_multiplier
            current_pipe.diameter = SMALL_PIPE_DIAMETER*SMALL_PIPE_DIAMETER_multiplier
        

    # Set the mystery parameters of our pipes

    for every_pipe in pipe_list:
        current_pipe:wntr.network.Pipe = wn.get_link(every_pipe)
        current_pipe.roughness = theta[f"roughness_coeff_for_pipe_{every_pipe}"]   #error 3 solved here
        current_pipe.minor_loss = theta[f"Minor_loss_coeff_for_pipe_{every_pipe}"] #error 4 solved here



    #Mystery parameter of our pump

    #Flows = [x for x in range(0,MAX_POSSIBLE_FLOW,step=0.1)]
    Flows = np.linspace(0, MAX_POSSIBLE_FLOW, 20)   #this should work, pls confirm chatgpt, error 5 solved here
    Head  = [pump_headloss_a_coeff - pump_headloss_b_coeff* Q*Q for Q in Flows]
    
    wn.add_curve("MAIN_PUMP_HEADLOSS_CURVE","HEAD",list(zip(Flows,Head)))  #since wn will be reset anyway we can keep this
    
    #atached the curve to the pump
    Mp:wntr.network.Pump = wn.get_link("Main_Pump")
    Mp.pump_curve_name="MAIN_PUMP_HEADLOSS_CURVE"                      #wn is a fresh network everytime 
                                                                       #this func is called so no need to remove
                                                                       # the curve ig
                                                             








@use_named_args(space)
def objective(**theta):
    wn = build_water_network()
    modify_network_for_this_sim(theta,wn)      # we will get a fresh default wn every time
    sim = wntr.sim.WNTRSimulator(wn)
                        
    results = sim.run_sim()

    flows = results.link["flowrate"].iloc[0]    # WE MSUT RPLACE 0 with a value..such that at that time , the 
                                                # network has achieved a steady flow state
    
    errors = []
    for pid in wn.pipe_name_list:
        errors.append(flows[pid] - MEASURED_FLOWS[pid])   #for now assuming we are measuinrg each pipe

    rmse = np.sqrt(np.mean(np.square(errors)))
    return rmse



result = gp_minimize(
    objective,
    space,
    n_calls=60,
    n_initial_points=15,
    random_state=42
)


calibrated = dict(zip([s.name for s in space], result.x))

with open("calibrated_params.yml", "w") as f:
    yaml.safe_dump(calibrated, f)

print("Best RMSE:", result.fun)
print("Parameters written to calibrated_params.yml")







        
        
        










