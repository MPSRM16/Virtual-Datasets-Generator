from abc import ABC, abstractmethod
from dataclasses import dataclass
import subprocess



class Deployer(ABC):
    output_r1: str
    output_r2: str
    name: str

    @property
    @abstractmethod #obriga sempre a que toda classe deve implementar
    def command(self):
        pass

    def deploy(self):
        process= subprocess.run(self.command, shell=True)
        output = process.stdout
        error = process.stderr

        if process.returncode != 0: #return code diferent de algo zero que dizer que teve um problema a correr
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")

@dataclass
class ArtArgs:
    r1: str
    r2: str
    len_of_reads: int
    size_of_sample: int
    sd: float
    number_of_reads: int
    fasta_file: str
    output_prefix: str

    def __str__(self) -> str:
        return (
            f"r1: {self.r1}, r2: {self.r2}"
        )


class ArtLauncher(Deployer):
    name= "Art"

    def __init__(self, args: ArtArgs):
        self.args = args

        self.output_prefix= f"{self.args.output_prefix}_{self.name}_"

        ######
        self.output_r1 = f"{self.output_prefix}1.fq"
        self.output_r2 = f"{self.output_prefix}2.fq"

        self.output_aln1= f"{self.output_prefix}'1.aln"
        self.output_aln2= f"{self.output_prefix}'2.aln"
    
    @property
    def command(self): #TODO number of reads que pensavamos que tavamos a passar é na verdade o fold read coverage por isso se trocarmos no comando maybe conseguimos passar o mesmo nos 2 trocar o f no comando para m com sorte basta fazer issoS
        
        return f"art_illumina -1 {self.args.r1} -2 {self.args.r2} -c {self.args.number_of_reads} -l {self.args.len_of_reads} -p -o {self.output_prefix} -m {self.args.size_of_sample} -s {self.args.sd} -i {self.args.fasta_file}"
#TODO passar mais um argumento aqui no comando pq o que está a ser passado como number of reads e a mean sample sizer nao é o sample size mas o fold read covegrage trocar o f pelo c no comando deve dar fix a tudo mas naos sei

@dataclass
class NanosimArgs:
    rg : str
    model_prefix : str
    output_prefix : str
    number_of_reads : int
    max_len : int
    min_len: int
    min_poly_len : int
    base_quality : float
    strandness: float
    dna_type : str
    num_threads : int
    


class NanosimLauncher(Deployer):
    name = "Nanosim"

    def __init__(self, args: NanosimArgs):
        self.args = args
        self.output_prefix = f"{self.args.output_prefix}_{self.name}"

        self.output_r1 = f"{self.output_prefix}_unaligned_reads.fasta"
        self.output_r2 = f"{self.output_prefix}_unaligned_reads.fasta"


    @property
    def command(self):
        cmd= f"simulator.py genome -rg {self.args.rg} -c {self.args.model_prefix} -o {self.output_prefix} -n {self.args.number_of_reads} -max {self.args.max_len} -min {self.args.min_len} -k {self.args.min_poly_len} -b {self.args.base_quality} -s {self.args.strandness} -d {self.args.dna_type} -t {self.args.num_threads}" 
        
        return cmd