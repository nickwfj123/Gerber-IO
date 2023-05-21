import pandas as pd
import numpy as np
import os
import re
import string

from datetime import datetime, date


def main(args4main):
    base = pd.read_csv(args4main['master'])
    data_dir = args4main['manifest']
    
    folders = os.walk(data_dir)
    
    for (dirpath, dirname, filename) in folders:
        for name in dirname:
            fd_path = data_dir + '/' + name
            name = name.lower()
            path = 'data_' + name + '_' + 'path'
            status =  'data_' + name + '_' + 'status'

            if path in base.columns:
                files = os.walk(fd_path)
                print('reading folder:', fd_path)
                for (dirpath, dirname, filename) in files:
                    fd_checker = dirpath.split('/')
                    if fd_checker[-3] == 'manifest' and fd_checker[-2].lower() in fd_checker[-1].lower():
                        for f in filename:
                            if f[:7] == 'samples' and os.path.splitext(f)[1] == '.csv':
                                print('- reading file: ', dirpath + '/' + f)
                                input_file = pd.read_csv(dirpath + '/' + f)
                                input_file.columns = input_file.columns.str.lower()
                                path_series = base['root_tree'].map(input_file.drop_duplicates('root_tree', keep='last').set_index('root_tree')['path']).dropna()

                                for index, value in path_series.items():
                                    base.loc[index, path] = value 
                        break

                base.loc[base[path].notnull(), status] = '2 Manifest generated'
                base.loc[base[path].isnull(), status] = '0 Raw data not available'
            
        break

    base.to_csv('final_output.csv', index=False, na_rep='NULL')

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--master', required = True, type=str)
    parser.add_argument('--manifest', required = True, type=str)
    
    args = parser.parse_args()
    
    args4main =	{
		'master': args.master.strip(),
        'manifest': args.manifest.strip(),
		}
        
    main(args4main)
