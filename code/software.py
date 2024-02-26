


from abc import ABC, abstractmethod
from code.process import ArtArgs, ArtLauncher, Deployer, NanosimArgs, NanosimLauncher
from typing import Dict, List

class SoftwareInterface(ABC):
    launcher_list: List[Deployer]
    launcher: Deployer
    name: str

    @abstractmethod
    def arg_verifier(self, config) -> bool:
        pass
        
    def return_deployer(self):
        return self.launcher

    @abstractmethod
    def extract_args(self, ref_path: str,  number_of_reads: int, output_prefix: str):
        pass

    @abstractmethod
    def init_launcher(self, software_args) -> Deployer:
        pass

    @abstractmethod
    def prep_args(self, config):
        pass
    
    def my_launcher(self, ref_filepath, number_of_reads, output_prefix):
        
    
        my_args = self.extract_args(ref_filepath, number_of_reads, output_prefix)
        

        my_launcher= self.init_launcher(my_args)

        #deploys the simulation
        my_launcher.deploy()

        #Saves the launches of the different simulation on a dictionary
        self.launcher_list.append(my_launcher)
    
    def arg_verify_and_prep(self, config) -> bool:

        success= self.arg_verifier(config=config)

        self.prep_args(config)

        return success




class ArtSoftware(SoftwareInterface):

    launcher= ArtLauncher
    args= ArtArgs
    name= "Art" 

    def __init__(self):
        self.launcher_list= []
        self.my_args= {}

    def arg_verifier(self,config) -> bool:
        """Verifys that all the arguments to run the Art software were given """
    
        if config['ART_ARGUMENTS'] is None:
            return  False

        fixed_arguments_dict = {
            "r1": None,
            "r2": None,
            "len_of_reads": None,
            "size_of_sample": None,
            "sd": None,
        }

        for key in config['ART_ARGUMENTS'].keys():
            if key in fixed_arguments_dict.keys():
                fixed_arguments_dict[key] = config['ART_ARGUMENTS'][key]
        if None in fixed_arguments_dict.values():
            raise ValueError("The following arguments are missing: {}".format(fixed_arguments_dict.keys()))#nao sei se isto continua a fazer sentido

        else:
            return True
    
    def prep_args(self, config):
        """Prepares the dictonary my_args for a specific software"""

        try:
            self.my_args= config['ART_ARGUMENTS']
        except KeyError as e:
            raise e
        
    def extract_args(self, ref_path: str, number_of_reads: int, output_prefix: str) -> dict:
        software_args = ArtArgs(
            self.my_args['R1'],
            self.my_args['R2'],
            int(self.my_args['len_of_reads']),
            int(self.my_args['size_of_sample']),
            float(self.my_args['sd']),
            number_of_reads,
            ref_path,
            output_prefix= output_prefix

        )

        return software_args
        

    def init_launcher(self, software_args: ArtArgs):
        """Initializes the Art launcher by giving it the arguments it needs"""

        launcher= ArtLauncher(software_args)

        return launcher



class NanosimSoftware(SoftwareInterface):

    launcher= NanosimLauncher
    args= NanosimArgs
    name= "NanoSim" 

    def __init__(self):
        self.my_args = {}
        self.launcher_list= []
        pass

    def arg_verifier(self,config) -> bool:
        """Verifys that all the arguments to run the Nanosim software were given """
        if config['NANOSIM_ARGUMENTS'] is None:
            return  False
        
        nanosim_arguments_dict = {
            "model_prefix": None,
            #"number_of_reads": None,
            "max_len": None,
            "min_len": None,
            "min_poly_len": None,
            "base_quality": None,
            "strandness": None,
            "dna_type": None,
            "num_threads": None
        }
        for key in config['NANOSIM_ARGUMENTS']:
            if key in nanosim_arguments_dict.keys():
                nanosim_arguments_dict[key] = config['NANOSIM_ARGUMENTS'][key]
        if None in nanosim_arguments_dict.values():
            raise ValueError("The following arguments are missing: {}".format(nanosim_arguments_dict.keys()))

        else:
            
            return True

    def prep_args(self, config):

        try:
            self.my_args= config['NANOSIM_ARGUMENTS']
        except KeyError as e:
            raise e

    def extract_args(self, ref_path: str,  number_of_reads: int, output_prefix: str) -> dict:

        software_args = NanosimArgs(
            ref_path,
            self.my_args['model_prefix'],
            output_prefix,
            number_of_reads,
            int(self.my_args['max_len']),
            int(self.my_args['min_len']),
            int(self.my_args['min_poly_len']),
            (self.my_args['base_quality']),
            float(self.my_args['strandness']),
            (self.my_args['dna_type']),
            int(self.my_args['num_threads'])
        )

        return software_args
    
    
    def init_launcher(self, software_args: NanosimArgs):
        """Initializes the Nanosim launcher by giving it the arguments it needs"""

        launcher= NanosimLauncher(software_args)

        return launcher
    
