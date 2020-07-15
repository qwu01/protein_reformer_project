
REM python src/protein_reformer/build_configs.py

python src/protein_reformer/run_language_modeling.py ^
    --output_dir=output/large_training_set/ ^
    --model_type=reformer ^
    --config_name=configs/large_training_set ^
    --tokenizer_name=configs/large_training_set ^
    --line_by_line ^
    --do_train ^
    --train_data_file=data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_train.txt ^
    --num_train_epochs 500 ^
    --warmup_steps 10000 ^
    --do_eval ^
    --eval_data_file=data/uniprot_sprot_LONG_SEQ_REMOVED/long_seq_removed_val.txt ^
    --logging_steps 500 ^
    --block_size 2560 
