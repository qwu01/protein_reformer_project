import glob
import random, codecs


def split_file(file,out1,out2,percentage=0.75,isShuffle=True,seed=42):
    """[summary]
        # split_file("data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed.txt", 
        #     "data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_train.txt",
        #     "data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_val.txt",
        #     percentage=0.9)
    Args:
        file ([type]): [description]
        out1 ([type]): [description]
        out2 ([type]): [description]
        percentage (float, optional): [description]. Defaults to 0.75.
        isShuffle (bool, optional): [description]. Defaults to True.
        seed (int, optional): [description]. Defaults to 42.
    """
    random.seed(seed)
    with codecs.open(file, 'r', "utf-8") as fin, \
         codecs.open(out1, 'w', "utf-8") as foutBig, \
         codecs.open(out2, 'w', "utf-8") as foutSmall:
        nLines = sum(1 for line in fin)
        fin.seek(0)

        nTrain = int(nLines*percentage) 
        nValid = nLines - nTrain

        i = 0
        for line in fin:
            r = random.random() if isShuffle else 0 # so that always evaluated to true when not isShuffle
            if (i < nTrain and r < percentage) or (nLines - i > nValid):
                foutBig.write(str(line))
                i += 1
            else:
                foutSmall.write(str(line))


def merge_tsv_files(files_path:str, output_path:str):
    """[summary]

    Args:
        files_path (str): [file path with wildcard, e.g. './data/uniprot_sprot.fasta/*.tab']
        output_path (str): [path/to/output.tsv]
    """
    interesting_files = glob.glob(files_path)
    print(f'merge {len(interesting_files)} files')

    header_saved = False

    with open(output_path,'w') as f_out:

        for filename in interesting_files:

            with open(filename) as f_in:
                header = next(f_in)
                if not header_saved:
                    f_out.write(header)
                    header_saved = True
                for line in f_in:
                    f_out.write(line)