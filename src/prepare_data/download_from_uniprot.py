import requests
import pandas as pd
from multiprocessing import Pool


def download_accession(accession):

    columns = [
        'id', # Entry
        'entry name', # Entry name
        'organism', # Organism
        'organism-id', # Organism id
        'length', # Length
        'mass', # Mass
        'go(biological process)',
        'go(molecular function)',
        'go(cellular component)',
        'sequence', # Sequence
    ]

    query_arg = {
        'query': 'accession:' + ' OR '.join(accession),
        'format': 'tab',
        'columns': ','.join(columns)
    }

    result = requests.get('http://www.uniprot.org/uniprot/', params=query_arg)
    return result

def get_chunks(accession_list, n_per_chunk):
    chunked_accessions_list = list()
    for i in range(0, len(accession_list), n_per_chunk):
        chunked_accessions_list.append(accession_list[i:i+n_per_chunk])
    return chunked_accessions_list

if __name__ == '__main__':

    df = pd.read_csv("data/uniprot_sprot.fasta/out.csv", header=None)

    accessions_list = list(df[0])
    chunked_accessions_list = get_chunks(accessions_list, n_per_chunk=400)
    for i in range(1250, len(chunked_accessions_list), 50):
        print(len(chunked_accessions_list))
        chunked_chunked_accessions_list = chunked_accessions_list[i:i+50]
        print(list(range(len(chunked_accessions_list)))[i: i+50])

        tmp = []
        header = "Entry\tEntry name\tOrganism\tOrganism ID\tLength\tMass\tGene ontology (biological process)\tGene ontology (molecular function)\tGene ontology (cellular component)\tSequence\n"
        tmp.append(header)

        with Pool(10) as p:
            res = p.map(download_accession, chunked_chunked_accessions_list)

        for result in res:
            tmp.append(result.text.replace(header, ''))
        
        results = ''.join(tmp)

        with open(f'data/uniprot_sprot.fasta/full{i}.tab', 'wt') as out_f:
            print(results, file=out_f)
        # results = ""
        # header = "Entry\tEntry name\tOrganism\tOrganism ID\tLength\tMass\tGene ontology (biological process)\tGene ontology (molecular function)\tGene ontology (cellular component)\tSequence\n"
        # results += header

        # with Pool(10) as p:
        #     res = p.map(download_accession, chunked_chunked_accessions_list)

        # for result in res:
        #     results += result.text.replace(header, '')

        # with open(f'data/uniprot_sprot.fasta/full{i}.tab', 'wt') as out_f:
        #     print(results, file=out_f)
