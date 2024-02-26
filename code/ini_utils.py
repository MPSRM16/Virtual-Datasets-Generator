
import pandas as pd
import os
import configparser
from typing import Dict, List
from code.software import NanosimSoftware, ArtSoftware, SoftwareInterface


class ReferenceInput:

    software_known_dict: Dict[str, SoftwareInterface]= {
        'nanosim': NanosimSoftware,
        'art': ArtSoftware
    }

    def __init__(self, filename: str= 'config.ini'):
        self.config = configparser.ConfigParser()
        self.read_ini(filename)
        self.filename = filename
        self.software_request_list= []
        self.software_to_run: List[SoftwareInterface]= self.valid_software_extract()

        print("Software Request: {}".format(self.software_request_list))
        print("Software to run: {}".format(self.software_to_run))   

        ############################################
        self.path_varifier()
        self.reference_path_verifier()
        self.proportion_verifier()
    
    def software_request_extract(self):
        """Extract software requests from the .ini file"""
        for value in self.config['SOFTWARE_REQUEST'].values():
            self.software_request_list.append(value.lower())

    def read_ini(self,filename: str):
        """Read the .ini file"""
        try:
            self.config.read(filename)
        except FileNotFoundError:
            raise ValueError(f"{filename} does not exist")
        

    def software_launcher_retrieve(self):
        pass
    

    def valid_software_extract(self) -> List[SoftwareInterface]:
        accepted_software_list = []

        for value in self.config['SOFTWARE_REQUEST'].values():

            if value not in self.software_known_dict.keys():
                continue

            software_interface: SoftwareInterface = self.software_known_dict[value]()
            print("validating software interface")
            if software_interface.arg_verify_and_prep(self.config):

                accepted_software_list.append(software_interface)

        if len(accepted_software_list) == 0:
            raise ValueError(f"{self.config['SOFTWARE_REQUEST']} is not a valid software request")
        
        return accepted_software_list
            
        
    def ini_arg_checker(self):
        for key in self.software_known_dict.keys():
            if key in self.config['SOFTWARE_REQUEST'].keys():
                pass


    @property
    def read_df_path(self) -> str:
        """Return the path to the csv file"""
        return self.config['FIXED_ARGUMENTS']['csv_path']


    def path_varifier(self) -> bool:
        """Check if the path to the csv file exists."""
        if os.path.exists(self.read_df_path):
            return True
        else:
            raise ValueError("Path to the .csv file does not exist")

    
    def proportion_verifier(self) -> bool:
        """Check if the proportion of the csv file add up to 1"""

        df = self.read_df()
        
        if df['proportion'].sum() != 1:
            raise ValueError(f"The proportion of reads is not equal to 1")
    
        return True
    
    def reference_path_verifier(self) -> bool:
        """Check if all the refrences path in the csv file exist"""
        df = self.read_df()
        for path in df["filepath"]:
            if os.path.exists(path):
                return True
            else:
                raise ValueError("Path to the refrence genome file does not exist")

    def read_proportions(self):
        """ Returns the proportions from the Dataframe"""
        if self.proportion_verifier():
            return self.read_df()['proportion']
        else:
            return None

    def read_df_paths(self) -> str:
        """Return the path to the diferent fasta files"""
        if self.reference_path_verifier:
            return self.read_df()['filepath']
        

    def read_df(self):
        """Read and creates the data frame from the path provided by the .ini file."""
        if self.path_varifier():
            if self.read_df_path.endswith(".csv"):
                return pd.read_csv(self.read_df_path)
            elif self.read_df_path.endswith(".tsv"):
                return pd.read_csv(self.read_df_path,sep="\t")
