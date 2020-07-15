
REM python src/protein_reformer/build_configs_large_dataset_3000_tokenizer.py

python src/protein_reformer/run_language_modeling.py ^
    --output_dir=output/large_training_set_with_3000_tokenizer/ ^
    --model_type=reformer ^
    --model_name_or_path=output/large_training_set_with_3000_tokenizer/checkpoint-54000 ^
    --tokenizer_name=configs/large_training_set_with_3000_tokenizer ^
    --line_by_line ^
    --do_train ^
    --train_data_file=data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_train.txt ^
    --warmup_steps 10000 ^
    --max_steps 1000000 ^
    --do_eval ^
    --eval_data_file=data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_val.txt ^
    --logging_steps 100 ^
    --block_size 2560 ^
    --overwrite_output_dir