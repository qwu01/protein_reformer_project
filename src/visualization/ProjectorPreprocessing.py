import pickle
import pandas as pd
import networkx as nx
'''
Maps ORF names to gene symbols (optional) in embedding and returns 
feature vector file and metadata file for use in TensorFlow Projector.
https://projector.tensorflow.org/
'''
class ProjectorPreprocessing:
    def __init__(self,
                 embedding_path,
                 out_path,
                 input_paths=[],
                 input_names=[],
                 id_mapping_path=None,
                 is_network=False):
        """TODO
        args:
            embedding_path (str): Path to embedding predicted by model.
            out_path (str): Path to save formatted files to.
            input_paths (list of str): Paths to input datasets integrated to create embedding.
            input_names (list of str): Names of corresponding input datasets.
            id_mapping_path (str): Path to id mapping dictionary pickle (ORF to Symbol).
            is_network (bool): Whether the input embedding is actually a network.
        """
        assert len(input_paths) == len(input_names)
        self.emb, self.id_mapper, self.inputs = self._load(embedding_path, id_mapping_path, input_paths, is_network)
        self.out_path = out_path
        self.input_names = input_names
        if id_mapping_path is not None:
            self._id_map()
        # self.metadata = self._get_metadata()
        self._save()
    def _load(self, embedding_path, id_mapping_path, input_paths, is_network=False):
        if is_network:
            emb = nx.to_pandas_adjacency(nx.read_weighted_edgelist(embedding_path))
        else:
            emb = pd.read_csv(embedding_path, index_col=0)
        if id_mapping_path is None:
            id_mapper = None
        else:
            id_mapper = pickle.load(open(id_mapping_path, 'rb'))
        inputs = [pd.read_csv(path, sep=' ', header=None) for path in input_paths]
        return emb, id_mapper, inputs
    def _id_map(self):
        """
        """
        # First remove any indices that are not in `self.id_mapper`.
        common_idxs = [idx for idx in self.emb.index if idx in self.id_mapper]
        self.emb = self.emb.reindex(common_idxs)
        # Next map each index using `self.id_mapper` by taking first mapping
        # in resulting list of possible mappings.
        mapped_idxs = [self.id_mapper[idx][0] for idx in self.emb.index]
        self.emb.index = mapped_idxs
    def _get_metadata(self):
        """
        """
        # First, get identifiers from `self.inputs` which are edge-lists.
        idxs = [set(df[0]).union(set(df[1])) for df in self.inputs]
        # Map IDs to corresponding symbols.
        idxs = [[self.id_mapper[idx][0] for idx in idxs_ if idx in self.id_mapper] for idxs_ in idxs]
        # Create corresponding set.
        idxs_set = [set(idxs_) for idxs_ in idxs]
        # Create a DataFrame of occurences (i.e. is a given identifier in the embedding
        # in the original input, for all inputs).
        occurences = []
        for idx in self.emb.index:
            occurences.append([1 if idx in idxs_ else 0 for idxs_ in idxs])
        # Get list of indices that are unique to each dataset.
        unique_idxs_sets = []
        for i, idxs_ in enumerate(idxs):
            unique = idxs_set[i].copy()
            dataset_positions = list(range(len(self.inputs)))
            dataset_positions.remove(i)
            for pos in dataset_positions:
                unique -= idxs_set[pos]
            unique_idxs_sets.append(unique)
        unique_idxs = []
        for idx in self.emb.index:
            unique_idxs.append([1 if idx in idxs_ else 0 for idxs_ in unique_idxs_sets])
        occurences = pd.DataFrame(occurences,
                                  index=self.emb.index,
                                  columns=[f'in_{name}' for name in self.input_names])
        occurences.index.name = 'names'
        unique_occurences = pd.DataFrame(unique_idxs,
                                         index=self.emb.index,
                                         columns=[f'unique_to_{name}' for name in self.input_names])
        unique_occurences.index.name = 'names'
        metadata = pd.concat([occurences, unique_occurences], axis=1)
        return metadata
    def _save(self):
        """Outputs mapped embedding features and metadata for use in 
        TensorFlow Projector.
        """
        # Output features.
        self.emb.to_csv(self.out_path + '_features.tsv', sep='\t', index=False, header=False)
        # Output metadata.
        pd.DataFrame(self.emb.index).to_csv(self.out_path + '_metadata.tsv', sep='\t', index=False, header=False)