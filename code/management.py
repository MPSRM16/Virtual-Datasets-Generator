"""
This script is used to simulate a mixture of samples from a reference panel.

The script takes an input configuration file that contains the parameters for the simulation.
The configuration file should be in INI format and have the following sections:

[General]
number_of_reads = 100000
output_directory = output/

[Sample1]
proportion = 0.5
filepath = sample1.fa

[Sample2]
proportion = 0.3
filepath = sample2.fa

[Sample3]
proportion = 0.2
filepath = sample3.fa

After reading the configuration file, the script will simulate the mixture of samples.
It will create a directory in the output directory for each simulation, and within each simulation directory,
it will create two files (R1.txt and R2.txt) that contain the simulated reads.

Finally, the script will concatenate all the R1.txt files and all the R2.txt files into two new files (my_r1.fq.gz and my_r2.fq.gz),
and compress them using gzip.

Note that this is just an example script, and you may need to modify it to fit your specific needs.
"""
from code.software import SoftwareInterface 
from code.ini_utils import ReferenceInput
from typing import List 
import os
import numpy as np
import shutil
import xopen


class Management:
    """
    This class is used to manage the simulation process.
    It reads the configuration file, sets up the directories, deploys the simulations,
    and concatenates and compresses the output files.
    """
    config_path: str
    output_directory: str
    ini_parser: ReferenceInput
    software_list: List[SoftwareInterface]
    output_r1_name: str
    output_r2_name: str

    final_output_directory = "sim_output"
    intermediate_dirname = "intermediate"

    def __init__(self, config_path, output_directory):
        """
        Initialize the class.

        Args:
            config_path (str): The path to the configuration file.
            output_directory (str): The directory where the output files will be saved.
        """
        self.config_path = config_path
        self.output_directory = output_directory

        self.ini_parser = ReferenceInput(self.config_path)

        self.fixed_parameters = self.ini_parser.config['FIXED_ARGUMENTS']

        self.software_list= self.ini_parser.software_to_run

        # Output file names
        self.output_r1_name = "my_r1.fq"
        self.output_r2_name = "my_r2.fq"

        # Output file paths
        self.output_r1_file_path = os.path.join(self.output_directory, self.output_r1_name)
        self.output_r2_file_path = os.path.join(self.output_directory, self.output_r2_name)
        self.intermediate_dirpath = os.path.join(self.output_directory, self.intermediate_dirname)
        self.outfile_directory= os.path.join(self.output_directory, self.final_output_directory)
        self.intermediate_directories_setup()


    def intermediate_directories_setup(self):
        self.my_dirs= {}
        for row_index, ref_row in self.ini_parser.read_df().iterrows():
            sim_name = f"sim_{row_index}"
            simulation_dirpath = os.path.join(self.intermediate_dirpath, sim_name)
            output_prefix = os.path.join(simulation_dirpath, f"sim_output_{row_index}") 
            os.makedirs(simulation_dirpath, exist_ok=True)
            self.my_dirs[row_index] = {
                "sim_name": sim_name,
                "simulation_dirpath": simulation_dirpath,
                "output_prefix": output_prefix
            }

    def setup_directories(self):
        """
        Create the output directory and the intermediate directory if they don't exist.
        """

     
        os.makedirs(self.output_directory, exist_ok=True)
        
        os.makedirs(self.intermediate_dirpath, exist_ok=True)
        
        os.makedirs(self.outfile_directory, exist_ok= True)


    def deploy_simulations(self):
        """
        Deploy the simulations.

        Args:
            intermediate_dirpath (str): The path to the intermediate directory.
        """
        total_number_of_reads = int(self.fixed_parameters["number_of_reads"])
        for row_index, ref_row in self.ini_parser.read_df().iterrows():
            
            if np.isnan(ref_row.proportion):
                continue

            proportion = float(ref_row.proportion)
            number_of_reads = int(total_number_of_reads * proportion)
            ref_filepath= ref_row.filepath
            
            output_prefix= self.my_dirs[row_index]["output_prefix"]

            for software in self.software_list:
                software.my_launcher(ref_filepath, number_of_reads, output_prefix)

    def concat_and_compress(self, input_file_path, outfile_path):
        """Compress and concatenate the given input file"""
        try:  
            with xopen.xopen(outfile_path, 'ab') as outfile:
                # Open the source file in read mode with xopen.
                with xopen.xopen(input_file_path, 'rb') as f:
                    # Read from the source file and append to the target file.
                    content= f.read()
                    if not content.endswith(b"\n"):
                        content + b"\n"
                    outfile.write(content)
            
        except Exception as e:
            print(e)
            raise FileNotFoundError(f"Not able to find {input_file_path} to concatenate")
        

    def concat_and_compress_all_sims(self):
        """
        Loop thorugh the output files to concatenate and compress them.
        """

        for software_interface in self.software_list:
            print(f"compressing {software_interface.name}")
            outfile_prefix = os.path.join(                          #MUDAR PARA a função dos paths?
            self.outfile_directory, software_interface.name) 
            
            oufile_r1= f"{outfile_prefix}_r1.fq.gz"
            oufile_r2= f"{outfile_prefix}_r2.fq.gz"

            for launcher in software_interface.launcher_list:

                self.concat_and_compress(launcher.output_r1,oufile_r1)
                self.concat_and_compress(launcher.output_r2,oufile_r2)  #falar com o joao sobre qual concat ficamos


    def ini_backup(self):
        """Makes a backyou of the Ini input file and saves it"""
        self.input_backup_path = f"input_backup"
        os.makedirs(self.input_backup_path, exist_ok=True)
        ini_file_path = self.ini_parser.filename
        shutil.copy(ini_file_path, self.input_backup_path)


    def df_backup(self):
        """Makes a backup of the data frame and saves it"""
        #TODO verificar se isto faz algo ou é para apagar
        shutil.copy(self.ini_parser.read_df_path, self.input_backup_path)
       
    def run(self):
        """
        Run the simulation.
        """
        self.ini_backup()

        self.df_backup()

        self.setup_directories()

        self.deploy_simulations()
        
        self.concat_and_compress_all_sims()