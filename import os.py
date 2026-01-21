import os
import yaml
import wntr

#constant Values
INITIAL_MAIN_TANK_LEVEL = 100  #yet to be measured
MAX_MAIN_TANK_LEVEL = 1000 #yet to be measured
MAIN_TANK_DIAMETER  = 100  #yet to be emasured
DEFAULT_PIPE_LENGTH = 154 #cm
SMALL_PIPE_DIAMETER = 20  #mm
BIG_PIPE_DIAMETER   = 50 #mm
DEFAULT_PIPE_ELEVATION = 75 #cm yet to be meausred
PUMP_TO_OUTLET_VERTICAL_PIPE_LENGTH = 20 #cm, yet to be measured
TANK_TO_PUMP_PIPE_ELEVATION = 10 #cm, yet to be measured
TANK_TO_PUMP_PIPE_LENGTH = 100 # cm, yet to be measutred






print(os.getcwd())
params = yaml.safe_load(open("parameter_values.yml"))


water_network = wntr.network.WaterNetworkModel()

water_network.add_tank("Main_Tank",init_level=INITIAL_MAIN_TANK_LEVEL,max_level=MAX_MAIN_TANK_LEVEL
                       ,diameter=MAIN_TANK_DIAMETER,overflow=False,coordinates=(20,20))

water_network.add_curve("c1","HEAD",[(20,20),(10,10),(0,0)])

water_network.add_junction("J1",elevation=TANK_TO_PUMP_PIPE_ELEVATION)

water_network.add_junction("J2",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pump("Main_Pump","J1","J2","HEAD","c1")
water_network.add_pipe("M1","Main_Tank","J1",TANK_TO_PUMP_PIPE_LENGTH,BIG_PIPE_DIAMETER)
water_network.add_junction("J3",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("M2","J2","J3",TANK_TO_PUMP_PIPE_LENGTH,BIG_PIPE_DIAMETER)
water_network.add_junction("J4",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("M3","J3","J4",diameter=BIG_PIPE_DIAMETER)
water_network.add_junction("J5",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P1","J4","J5",diameter=BIG_PIPE_DIAMETER)
water_network.add_junction("J6",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P2","J5","J6",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)
water_network.add_junction("J7",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P3","J6","J7",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)
water_network.add_junction("J8",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P4","J7","J8",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)
water_network.add_junction("J9",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P5","J8","J5",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH,initial_status="CLOSED")
water_network.add_pipe("P6","J8","J9",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)
water_network.add_junction("J10",elevation=DEFAULT_PIPE_ELEVATION)
water_network.add_pipe("P7","J9","J10",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)
water_network.add_pipe("P8","J10","Main_Tank",diameter=BIG_PIPE_DIAMETER,length=DEFAULT_PIPE_LENGTH)












wntr.network.write_inpfile(water_network,"Calibirated Network.inp")