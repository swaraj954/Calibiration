import os
import yaml
import wntr
import pandas as pd



CM = 0.01
MM = 0.001

INITIAL_MAIN_TANK_LEVEL = 100 * CM        #not measured in space
MAX_MAIN_TANK_LEVEL = 1000 * CM           # not measured in space
MAIN_TANK_DIAMETER = 100 * CM             #not measured 

DEFAULT_PIPE_LENGTH = 154 * CM             #not emasured in space
SMALL_PIPE_DIAMETER = 20 * MM              # in space
BIG_PIPE_DIAMETER = 50 * MM                # in space

DEFAULT_PIPE_ELEVATION = 75 * CM           # not measured  in space
TANK_TO_PUMP_PIPE_ELEVATION = 10 * CM      # not measured  in space
TANK_TO_PUMP_PIPE_LENGTH = 100 * CM        # not measured  in space
PUMP_TO_FIRST_BEND_PIPE_LENGTH = 100 * CM  #not measured   in space
FIRST_BEND_TO_GRID_PIPE_LENGTH = 100 * CM  #not measured   in space


def build_water_network():


    os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    wn = wntr.network.WaterNetworkModel()
    #wn.options.hydraulic.headloss = "H-W"  #no need it is there by default

    # ---- Tank ----
    wn.add_tank(
        "Main_Tank",
        init_level=INITIAL_MAIN_TANK_LEVEL,
        max_level=MAX_MAIN_TANK_LEVEL,
        diameter=MAIN_TANK_DIAMETER,
        overflow=False,
        coordinates=(20, 20)
    )

    # ---- Junctions ----
    wn.add_junction("J1", elevation=TANK_TO_PUMP_PIPE_ELEVATION,coordinates=(17,20))
    wn.add_junction("J2", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(15,20))
    wn.add_junction("J3", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,20))
    wn.add_junction("J4", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,18))
    wn.add_junction("J5", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,16))
    wn.add_junction("J5_1", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,14))
    wn.add_junction("J5_2", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,12))
    wn.add_junction("J5_3", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,10))
    wn.add_junction("J6", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(-1,0))
    wn.add_junction("J6_1", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(3,0))
    wn.add_junction("J6_2", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(7,0))
    #wn.add_junction("J6_3", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(10,0))
    wn.add_junction("J7", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,0))
    wn.add_junction("J7_1", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,3))
    wn.add_junction("J7_2", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,8))
    wn.add_junction("J7_3", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,10))
    wn.add_junction("J8", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,15))
    wn.add_junction("J9", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(16,17))
    wn.add_junction("J10", elevation=DEFAULT_PIPE_ELEVATION,coordinates=(19,17))

    # ---- Pipes ----
    wn.add_pipe("M1", "Main_Tank", "J1", TANK_TO_PUMP_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("M2", "J2", "J3", PUMP_TO_FIRST_BEND_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("M3", "J3", "J4", FIRST_BEND_TO_GRID_PIPE_LENGTH, BIG_PIPE_DIAMETER)

    wn.add_pipe("P1", "J4", "J5", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)

    wn.add_pipe("P2", "J5", "J5_1", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P2_1", "J5_1", "J5_2", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P2_2", "J5_2", "J5_3", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P2_3", "J5_3", "J6", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)

    wn.add_pipe("P3", "J6", "J6_1", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P3_1", "J6_1", "J6_2", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    #wn.add_pipe("P3_2", "J6_2", "J6_3", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    #wn.add_pipe("P3_3", "J6_3", "J7", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    #Correction:
    wn.add_pipe("P3_3", "J6_2", "J7", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)


    wn.add_pipe("P4", "J7", "J7_1", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P4_1", "J7_1", "J7_2", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P4_2", "J7_2", "J7_3", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P4_3", "J7_3", "J8", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)



    wn.add_pipe("P5", "J8", "J5", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER, initial_status="CLOSED")
    wn.add_pipe("P6", "J8", "J9", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P7", "J9", "J10", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)
    wn.add_pipe("P8", "J10", "Main_Tank", DEFAULT_PIPE_LENGTH, BIG_PIPE_DIAMETER)

    # ---- Pump ----
    wn.add_pump(name = "Main_Pump",start_node_name= "J1",end_node_name= "J2", pump_type="HEAD",pump_parameter="Filler_curve")
    wn.add_curve("Filler_curve","HEAD",[(0,0),(1,1),(2,2)])


    wntr.network.write_inpfile(wn,"test(one datapoint).inp")
    return wn


build_water_network()