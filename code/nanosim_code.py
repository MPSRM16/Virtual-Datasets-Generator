from dataclasses import dataclass
import os
from code.ini_utils import ReferenceInput
from code.process import Deployer

@dataclass
class NanosimArgs:
    rg : str
    model_prefix : str
    output_prefix : str
    number_of_reads : int
    max_len : int
    min_len: int
    #med_len : int
    #sd : float
    min_poly_len : int
    base_quality : float
    strandness: float
    dna_type : str
    num_threads : int
 



class NanosimReferenceOutput(ReferenceInput):

    INI_SECTION= "NANOSIM_ARGUMENTS"

    def __init__(self, filename: str= 'config.ini'):
        super().__init__(filename)

        self.path_varifier()
        self.reference_path_verifier()
        self.proportion_verifier()

    def check_if_model_profile_path_exists(self):
        if os.path.exists(self.config[self.INI_SECTION]['model_prefix']):
            return True
        else:
            return False
        
    def check_if_reference_genome_path_exists(self):
        if os.path.exists(self.config[self.INI_SECTION]['reference_genome']):
            return True
        else:
            return False
        
    def check_if_output_path_exists(self):
        if os.path.exists(self.config[self.INI_SECTION]['output']):
            return True
        else:
            return False
        
    #def check_if_sd_valid(self):
        return self.config['NANOSIM_ARGUMENTS']['sd'] > 0 
    
    def check_if_dna_type_valid(self):
        if self.config[self.INI_SECTION]['dna_type'] == 'linear':
            return True
        elif self.config[self.INI_SECTION]['dna_type'] =='circular':
            return True
        else:
            return False
        

class NanosimLauncher(Deployer):

    def __init__(self, args: NanosimArgs):
        self.args = args


    @property
    def command(self):
        
        return f"simulator.py genome -rg {self.args.rg} -c {self.args.model_prefix} -o {self.args.output} -n {self.args.number_of_reads} -max {self.args.max_len} -min {self.args.min_len} -k {self.args.min_poly_len} -b {self.args.base_quality} -s {self.args.strandness} -d {self.args.dna_type} -t {self.args.num_threads}"                                                                                                                                                                        