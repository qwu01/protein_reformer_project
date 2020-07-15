from transformers import ReformerConfig, ReformerTokenizer, ReformerModel
import sentencepiece as spm
import os


assert os.path.exists('configs/large_training_set/training_vocab.txt') == 1\
    , f'build a lower case amino acid txt file to train tokenizer. content should be: {"ARNDCQEGHILKMFPSTWYVOUBZX".lower()}'
MODEL_MAX_LENGTH = 2560

spm.SentencePieceTrainer.Train("--input=configs/large_training_set/training_vocab.txt --max_sentence_length=2550000 --model_prefix=spiece --vocab_size=30 --pad_id=29 --character_coverage=1.0")
os.system("mv spiece.model spiece.vocab configs/large_training_set")
tokenizer = ReformerTokenizer(vocab_file="configs/large_training_set/spiece.model", do_lower_case=True, truncation=True, model_max_length=MODEL_MAX_LENGTH)
tokenizer.save_pretrained("configs/large_training_set")

configuration = ReformerConfig.from_pretrained("google/reformer-crime-and-punishment")
configuration.axial_pos_shape = (40, 64)
configuration.max_position_embeddings=MODEL_MAX_LENGTH
configuration.vocab_size=tokenizer.vocab_size
configuration.pad_token_id=tokenizer.pad_token_id
configuration.output_hidden_states=True
configuration.save_pretrained('configs/large_training_set/')