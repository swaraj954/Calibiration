from outer_perimeter_structure_replica import *
import wntr

def build_full_water_network():

    os.chdir("C:\\Users\\SWARAJ SONAVANE\\Desktop\\Thesis work\\Simulations\\Calibiration")
    

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

    #add pipes
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
    #--------------------------------------------

    



    wntr.network.write_inpfile(outer_struc,"Full_Structure.inp")
    


build_full_water_network()
    