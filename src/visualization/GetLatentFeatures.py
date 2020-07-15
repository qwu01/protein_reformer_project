import requests
import pandas as pd
from multiprocessing import Pool
import sys, re, csv, codecs
from Bio import SeqIO
from transformers import ReformerConfig, ReformerTokenizer, ReformerModel, ReformerModelWithLMHead
import torch

class GetLatentFeatures(object):
    """[summary]

    Args:
        object ([type]): [description]
    """
    def __init__(self, df, tokenizer, model, save_tsv_path, use_cuda=True):
        """[summary]
            df: 
                id, sequence
                xx01, abcd
        Args:
            df ([pd.DataFrame]): [dataframe]
            tokenizer ([type]): [description]
            model ([type]): [description]
        """
        self._model = model.cuda() if use_cuda else model
        self._tokenizer = tokenizer
        self._df = df
        self._use_cuda = use_cuda
        self._save_tsv_path = save_tsv_path

        self.latent_features = self._go()
        self._save()

    def _go(self):
        sequence_list = list(self._df[1])
        if self._use_cuda:
            input_sequence_list = [self._tokenizer(sequence.strip(), truncation=True, return_tensors='pt')['input_ids'].cuda() for sequence in sequence_list] 
        else:
            input_sequence_list = [self._tokenizer(sequence.strip(), truncation=True, return_tensors='pt')['input_ids'] for sequence in sequence_list] 
        protein_vectors_list = [torch.mean(self._model(inp)[1][-1], dim=1) for inp in input_sequence_list]
        protein_vectors = torch.cat(protein_vectors_list, dim = 0)
        protein_vectors_numpy = protein_vectors.to('cpu').numpy()
        return protein_vectors_numpy

    def _save(self):
        latent_features_df = pd.DataFrame.from_records(self.latent_features)
        latent_features_df.to_csv(self._save_tsv_path, sep='\t', header=False, index=False)


    @classmethod
    def prepare_from_tsv_file(cls, tsv_file_path, tokenizer_vocab_file_path, model_checkpoint_path, save_tsv_path, use_cuda=True):
        """[summary]

        Args:
            tsv_file_path ([type]): [description]
            tokenizer_vocab_file_path ([type]): [description]
            model_checkpoint_path ([type]): [description]
            use_cuda (bool, optional): [description]. Defaults to True.
        """
        df = pd.read_csv(tsv_file_path, sep='\t', header=None)
        tokenizer = ReformerTokenizer(vocab_file="configs/alternative_tokenizer/alternative_tokenizer.model", do_lower_case=True, model_max_length=50000)
        model = ReformerModelWithLMHead.from_pretrained('output/alternative_tokenizer/checkpoint-100000')
        model.eval()
        return cls(df=df, tokenizer=tokenizer, model=model, save_tsv_path=save_tsv_path)


if __name__ == '__main__':
    GetLatentFeatures.prepare_from_tsv_file(tsv_file_path = 'data/to_embedding_projector/output.tsv',
                                            tokenizer_vocab_file_path = "configs/alternative_tokenizer/alternative_tokenizer.model", 
                                            model_checkpoint_path = 'output/alternative_tokenizer/checkpoint-100000',
                                            save_tsv_path = 'data/to_embedding_projector/latent_features.tsv')
