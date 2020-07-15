import argparse
import pandas as pd
import sys

def check_content(content:str, pattern:str):
    try:
        return pattern.lower() in content.lower()
    except:
        return None

def add_columns(pandas_df, add_column_list:list, based_on_column:str):
    for column in add_column_list:
        pandas_df[column]=[check_content(content, column) for content in pandas_df[based_on_column]]
    return pandas_df

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('from_file_path', help='Files to be modified (add localization columns)', type=argparse.FileType('r'))
    parser.add_argument('to_file_path', help='save modified file', type=argparse.FileType('w'))

    args=parser.parse_args(arguments)

    add_column_list = ['Cytoplasm', 'Nucleus','Mitochondrion','Endoplasmic', 'Golgi', 'Peroxisome','Endosome','Vacuole', 'Membrane']
    df = pd.read_csv(args.from_file_path, sep='\t')
    df = add_columns(pandas_df = df, add_column_list = add_column_list, based_on_column='Gene ontology (cellular component)')
    df.to_csv(args.to_file_path, sep='\t', index=False, line_terminator='\n')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))



