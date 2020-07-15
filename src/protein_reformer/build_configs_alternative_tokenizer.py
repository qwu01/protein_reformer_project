from transformers import ReformerConfig, ReformerTokenizer, ReformerModel
import sentencepiece as spm
import os


MODEL_MAX_LENGTH = 2560

spm.SentencePieceTrainer.Train("--input=data/uniprot_sprot.fasta/taste.txt --max_sentence_length=2550000 --model_prefix=alternative_tokenizer --vocab_size=3000 --pad_id=29 --character_coverage=1.0")
os.system("mv alternative_tokenizer.model alternative_tokenizer.vocab configs/alternative_tokenizer")
tokenizer = ReformerTokenizer(vocab_file="configs/alternative_tokenizer/alternative_tokenizer.model", do_lower_case=True, truncation=True, model_max_length=MODEL_MAX_LENGTH)
tokenizer.save_pretrained("configs/alternative_tokenizer")

configuration = ReformerConfig.from_pretrained("google/reformer-crime-and-punishment")
configuration.axial_pos_shape = (40, 64)
configuration.max_position_embeddings=MODEL_MAX_LENGTH
configuration.vocab_size=tokenizer.vocab_size
configuration.pad_token_id=tokenizer.pad_token_id
configuration.output_hidden_states=True
configuration.save_pretrained('configs/alternative_tokenizer/')