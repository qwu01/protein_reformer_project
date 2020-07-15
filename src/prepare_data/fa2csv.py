import sys, re, csv, codecs
from Bio import SeqIO

input_file_name = sys.argv[1] # data/input.fasta
output_file_name = sys.argv[2] # data/output.txt


with codecs.open(input_file_name, 'r', encoding='utf-8', errors='ignore') as f:
    output_list = []
    for record in SeqIO.parse(f, 'fasta'):
        id = re.search('\|(.*)\|', str(record.id)).group(1)
        seq = str(record.seq)
        output_list.append([id, seq])

with open(output_file_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_list)
