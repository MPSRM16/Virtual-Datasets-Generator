import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass
import subprocess




def argument_passer():
    parser = argparse.ArgumentParser(description='Simulation parameters')
    #TODO mundar para nomes que tu percebes minimamente
    #TODO criEar arg ini 
    #parser.add_argument('-rg', '--ref_g', type=str, required=True, help='Path to the to the input reference genome')
   
    parser.add_argument('-gl', '--genome_list ', type=int, required=True, help='Path to the  Reference metagenome list, tsv file')
    parser.add_argument('-a', '--abundance_list ', type=int, required=True, help='Path to the Abundance list, tsv file')
    parser.add_argument('-dl', '--dna_type_list ', type=int, required=True, help='Path to the DNA type list, tsv file')
    parser.add_argument('-c', '--model_prefix', type=str, required=True, help='Path and prefix of the error profile generated from the characterization step')
    parser.add_argument('-o', '--output ', type=int, required=True, help='Path to the output directory')
    #parser.add_argument('-n', '--number', type=str, required=True, help='Number of reads to be simulated')
    parser.add_argument('-max', '--max_len', type=int, required=True, help='The maximum length for the simulated reads')
    parser.add_argument('-min', '--min_len', type=float, required=True, help='The minimum length for the simulated reads')
    parser.add_argument('-med', '--median_len', type=int, required=True, help='The median length for the simulated reads')
    parser.add_argument('-sd', '--sd_len', type=float, required=True, help='The standard deviation of of the read lenght of the simulated reads')
    parser.add_argument('-k', '--min_poly_len', type=int, required=True, help='The minimum homopolymer lenght to simulate homopolymer contraction and expansion events')
    parser.add_argument('-b', '--base_quality', type=str, required=True, help='The simulate homopolymers and/or base qualities with respect to chosen basecaller: albacore, guppy, or guppy-flipflop')
    parser.add_argument('-s', '--strandness', type=float, required=True, help='The proportion of sense sequences. Overrides the value profiled in characterization stage. Should be between 0 and 1')
    #parser.add_argument('-dna', '--dna_type', type=str, required=True, help='The specify the dna type: circular OR linear')
    parser.add_argument('-t', '--num_threads', type=int, required=True, help='The number of threads for simulation')
    
    args = parser.parse_args()

    RG = args.read1
    R2 = args.read2
    len_of_reads = args.length
    name_of_file = args.name
    size_of_sample = args.size
    sd = args.standard_deviation
    number_of_reads = args.number_of_reads
    fasta_file = args.fasta

    #RG = args.ref_g
    #O = args.mode_prefix
    #N = args.output
    MAX = args.max_len 
    MIN = args.min_len
    MED = args.min_len
    SD = args.sd
    K = args.min_poly_len


    nanosim_args = NanosimArgs(
        rg = RG,
        r2=R2,
        len_of_reads=len_of_reads,
        name_of_file=name_of_file,
        size_of_sample=size_of_sample,
        sd=sd,
        number_of_reads=number_of_reads,
        fasta_file=fasta_file,
        output_prefix=name_of_file
    )

    return art_args





    

