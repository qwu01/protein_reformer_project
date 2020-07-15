
python src/protein_reformer/build_configs_alternative_tokenizer.py

python src/protein_reformer/run_language_modeling.py ^
    --output_dir=output/alternative_tokenizer/ ^
    --model_type=reformer ^
    --config_name=configs/alternative_tokenizer ^
    --tokenizer_name=configs/alternative_tokenizer ^
    --line_by_line ^
    --do_train ^
    --train_data_file=data/yeast/yeast_train.txt ^
    --warmup_steps 10000 ^
    --max_steps 100000 ^
    --do_eval ^
    --eval_data_file=data/yeast/yeast_val.txt ^
    --evaluate_during_training ^
    --logging_steps 100 ^
    --block_size 2560 