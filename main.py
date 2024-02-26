
from typing import List 
import numpy as np
from code.management import Management
import argparse


def arg_parser():
    parser = argparse.ArgumentParser(description='Simulation parameters')
    parser.add_argument('-c', '--config', type=str, default= "config.ini", help= "Path to the config.ini configuration file")
    parser.add_argument('-o', '--output', type=str, default= "simulation_output", help= "Path to the output directory")

    args = parser.parse_args()

    args_dict = {}
    args_dict['config'] = args.config
    args_dict['output'] = args.output

    return args_dict


def main():
    ############################################
    ############################################# section 0 : grab global args
    args_dict= arg_parser()
    my_config= args_dict['config']
    my_output_directory= args_dict["output"]

    my_manager = Management(my_config, my_output_directory)
    my_manager.run()

    ###########################################
    ############################################# section 1: prep total

    

if __name__ == "__main__":
    main()



    
        


        
