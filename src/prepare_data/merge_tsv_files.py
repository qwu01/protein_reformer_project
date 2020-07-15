import glob

interesting_files = glob.glob("./data/uniprot_sprot.fasta/*.tab")
print(f'merge {len(interesting_files)} .tab files')
header_saved = False

with open('./data/uniprot_sprot.fasta/full_all.tab','w') as f:
    for filename in interesting_files:
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                f.write(header)
                header_saved = True
            for line in fin:
                f.write(line)