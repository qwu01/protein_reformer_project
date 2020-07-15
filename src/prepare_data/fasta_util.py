import sys, re, csv, codecs
from Bio import SeqIO


def fasta2csv(input_file_name:str, output_file_name:str):
    """[extract protein id and sequence from .fasta file, save to .csv file]
    
    Args:
        input_file_name (str): [path/to/input.fasta]
        output_file_name (str): [path/to/output.csv]

    """
    with codecs.open(input_file_name, 'r', encoding='utf-8', errors='ignore') as f:
        output_list = []
        for record in SeqIO.parse(f, 'fasta'):
            id = re.search('\|(.*)\|', str(record.id)).group(1)
            seq = str(record.seq)
            output_list.append([id, seq])

    with open(output_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_list)

def fasta2txt(input_file_name:str, output_file_name:str):
    """[extract sequence from .fasta file, save to .txt file, one per line]

    Args:
        input_file_name (str): [path/to/input.fasta]
        output_file_name (str): [path/to/output.txt]
    """
    with codecs.open(input_file_name, 'r', encoding='utf-8', errors='ignore') as f:
        output_list = []
        for record in SeqIO.parse(f, 'fasta'):
            output_list.append(str(record.seq))

    with open(output_file_name, "w", encoding='utf-8') as file:
        for s in output_list:
            file.write("%s\n" % s.lower())