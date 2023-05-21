import pandas as pd
import numpy as np
import os
from datetime import date

def main(args4main):
    # load data
    data_dir = args4main['input']
    if not os.path.exists(data_dir):
        raise FileNotFoundError('Input data not found.')

    output_path = args4main['output']
    type = args4main['type']
    
    # list all files under data dir
    files = os.walk(data_dir)
    input_name = os.path.abspath(data_dir).split(os.sep)[-1]
    # record file names and paths
    names = []
    paths = []
    types = []

    for (dirpath, dirname, filename) in files:
        # skip the iteration if there are nested folders in subfolders of the root folder
        # path = dirpath.split(os.sep)
        # temp = path.index(input_name)
        # path = path[temp:]
        # if len(path) > 2:
        #     continue

        # iterate each file
        for f in filename:
            split_str = os.path.splitext(f)
            if split_str[1] and split_str[1] != '.DS_Store':
                if type == 'all':
                    names.append(f)   
                    paths.append(os.path.join(os.path.abspath(dirpath)))
                    types.append(split_str[1][1:].upper())
                else:
                    if f.endswith(type):
                        names.append(f)
                        paths.append(os.path.join(os.path.abspath(dirpath)))
                        types.append(type.upper())

    # create data frame
    df = pd.DataFrame()   
    df['seqid'] = names
    df['path'] = paths
    df['Type'] = types
    
    # create output folder
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    today = date.today()
    d = today.strftime("%Y%m%d")
    
    df.to_csv(output_path + '/' + d + '_' + type + '_result.csv', index=False)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', required = True, type=str,)
	parser.add_argument('--output', required = True, type=str,)
	parser.add_argument('--type', required = False, type=str, default='all')

	args = parser.parse_args()

	args4main =	{
		'input': args.input.strip(),
		'output': args.output.strip(),
        'type': args.type.strip(),
		}

	main(args4main)
