import pandas as pd
import numpy as np
import os
import re
import string

from datetime import datetime, date

def find_closest_time(days):
    if pd.isna(days):
        return np.nan
    if days == 0:
        return 'bl'
    dic = {'2w': 14, '3w': 21, '4w': 28, '6w': 42, '3m': 90, '6m': 180, '9m': 270, '12m': 360, '15m': 450, '18m': 540, 
    '21m': 630, '24m': 720, '27m': 810, '30m': 900, '33m': 990, '36m': 1080, '39m': 1170, '42m': 1260}
    closest = min(dic.items(), key=lambda x: abs(days - x[1]))
    return closest[0]


def main(args4main):
    data = pd.read_csv(args4main['input'])

    bl_queue = []
    # iterate by row
    for index, row in data.iterrows():
        # skip null value row
        if pd.isna(row['timepoint_std']):
            continue

        if row['timepoint_std'] == 'bl':
            if bl_queue:
                bl_queue.pop()
            bl_queue.append(row['date_std'])

        days_duration = (pd.to_datetime(row['date_std']) - pd.to_datetime(bl_queue[0])).days
        data.loc[index, 'days'] = days_duration
        data.loc[index, 'weeks'] = round(days_duration/7, 1)
        data.loc[index, 'months'] = round(days_duration/30, 1)
        data.loc[index, 'timepoint_std'] = find_closest_time(days_duration)
        
        # fill system_patient_id with 0
        tmp = row['system_patient_id'].split('_')
        tmp[2] = tmp[2].zfill(3)
        data.loc[index, 'system_patient_id'] = tmp[0] + '_' + tmp[1] + '_' + tmp[2]
    
    # final output table
    data.to_csv(args4main['output'] + '/biospecimen_updated.csv', index=False, na_rep='NULL')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str,)
    parser.add_argument('--output', required=True, type=str,)

    args = parser.parse_args()
    args4main = {
        'input': args.input.strip(),
        'output': args.output.strip(),
    }

    main(args4main)
