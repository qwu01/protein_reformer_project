import requests
import pandas as pd
from multiprocessing import Pool
import sys, re, csv, codecs
from Bio import SeqIO


class MetadataRetriever(object):
    """ Download metadata as labels. Download from uniprot. Save metadata to .tsv

    Args:
        object ([type]): [description]
    """
    def __init__(self, df, n_per_chunk=400, output_path='data/uniprot_sprot.fasta/full.tab'):
        """[summary]

        Args:
            df ([pd.DataFrame]): [description]
            n_per_chunk (int, optional): [description]. Defaults to 400.
            save_path (str, optional): Defaults to 'data/uniprot_sprot.fasta/full.tab'
        """
        self._base_url = 'http://www.uniprot.org/uniprot/'
        self._output_path = output_path

        self._columns = [
            'id', # Entry
            'entry name', # Entry name
            'organism', # Organism
            'organism-id', # Organism id
            'length', # Length
            'mass', # Mass
            'go(biological process)',
            'go(molecular function)',
            'go(cellular component)',
        ]

        self._df = df
        self._n_per_chunk = n_per_chunk
        self._forward(self._n_per_chunk, self._output_path)

    def _forward(self, n_per_chunk, output_path):
        """download from uniprot, save to .tab files.

        Args:
            n_per_chunk (int, optional): [description].
            output_path (str, optional): [description].
        """
        self._accession_list = list(self._df[0])
        self._chunked_accessions_list = self.get_chunks(self._accession_list, n_per_chunk=n_per_chunk)
        
        tmp = []
        header = "Entry\tEntry name\tOrganism\tOrganism ID\tLength\tMass\tGene ontology (biological process)\tGene ontology (molecular function)\tGene ontology (cellular component)\n"
        tmp.append(header)

        with Pool(10) as p:
            res = p.map(self.download_accession, self._chunked_accessions_list)

        for result in res:
            tmp.append(result.text.replace(header, ''))
        
        results = ''.join(tmp)

        with open(output_path, 'wt') as out_f:
            print(results, file=out_f)
        
        # makesure output rows have same order as fasta and csv files!
        out_df = pd.read_csv(output_path, sep='\t')
        out_df.set_index('Entry', inplace=True)
        out_df = out_df.loc[self._accession_list, :]
        out_df.reset_index(inplace=True)

        # maybe because of using Pool, some Entry are duplicated! remove duplicated Entries
        out_df = out_df.drop_duplicates()

        # save again
        out_df.to_csv(output_path, sep='\t')


    def download_accession(self, accession):
        """[summary]
        TODO: add retry.
        Args:
            accession ([type]): [description]

        Returns:
            res: [str]: [to be saved]
        """
        query_arg = {
            'query': 'accession:' + ' OR '.join(accession),
            'format': 'tab',
            'columns': ','.join(self._columns)
        }
        res = requests.get(self._base_url, params=query_arg)
        return res

    @staticmethod
    def get_chunks(accession_list, n_per_chunk):
        chunked_accessions_list = list()
        for i in range(0, len(accession_list), n_per_chunk):
            chunked_accessions_list.append(accession_list[i:i+n_per_chunk])
        return chunked_accessions_list
    
    @classmethod
    def from_fasta(cls, 
        fasta_path, 
        save_tsv=True, 
        delimiter='\t',
        tsv_output_path='data/uniprot_sprot.fasta/output.tsv', 
        n_per_chunk=400, 
        output_path='data/uniprot_sprot.fasta/full.tab'):
        """build metadata from fasta file.

        Args:
            fasta_path ([str]): [path/to/x.fasta]
        """
        with codecs.open(fasta_path, 'r', encoding='utf-8', errors='ignore') as f:

            output_list = []

            for record in SeqIO.parse(f, 'fasta'):
                id = re.search('\|(.*)\|', str(record.id)).group(1)
                seq = str(record.seq)
                output_list.append([id, seq])


        if save_tsv:
            with open(tsv_output_path, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerows(output_list)
        
        # df = pd.DataFrame(output_list, columns = ['id', 'seq'])
        df = pd.DataFrame(output_list)
        return cls(df, n_per_chunk, output_path)

if __name__ == '__main__':
    # MetadataRetriever.from_fasta(fasta_path='data/to_embedding_projector/input.fasta', 
    #     n_per_chunk=10, 
    #     tsv_output_path='data/to_embedding_projector/output.tsv', 
    #     output_path='data/to_embedding_projector/full.tab')
    MetadataRetriever.from_fasta(fasta_path='data/example/example.fasta', 
        n_per_chunk=10, 
        tsv_output_path='data/example/output.tsv', 
        output_path='data/example/full.tab')
    