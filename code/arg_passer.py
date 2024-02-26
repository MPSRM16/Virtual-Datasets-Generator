import argparse
from process import ArtArgs

def argument_passer():
    
    #TODO mundar para nomes que tu percebes minimamente
    #TODO criEar arg ini 
    parser.add_argument('-r1', '--read1', type=str, required=True, help='Path to the first read quality profile')
    parser.add_argument('-r2', '--read2', type=str, required=True, help='Path to the second read quality profile')
    parser.add_argument('-l', '--length', type=int, required=True, help='Length of reads to be simulated')
    parser.add_argument('-n', '--name', type=str, required=True, help='Name of the output file')
    parser.add_argument('-s', '--size', type=int, required=True, help='Mean size of the sample')
    parser.add_argument('-sd', '--standard_deviation', type=float, required=True, help='Standard deviation of the sample')
    parser.add_argument('-nr', '--number_of_reads', type=int, required=True, help='Number of reads to be simulated')
    
    parser.add_argument('-f', '--fasta', type=str, required=True, help='Filename of input DNA/RNA reference')

    args = parser.parse_args()

    R1 = args.read1
    R2 = args.read2
    len_of_reads = args.length
    name_of_file = args.name
    size_of_sample = args.size
    sd = args.standard_deviation
    number_of_reads = args.number_of_reads
    fasta_file = args.fasta

    art_args = ArtArgs(
        r1=R1,
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