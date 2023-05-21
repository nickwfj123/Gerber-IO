import pandas as pd
import numpy as np
import os
import re
import string

from datetime import datetime, date


def pid_extractor(str):
    for char in str:
        if char in string.punctuation and char != '-':
            return 'manual correction needed'

    if str.count('-') == 1:
        str = str.split('-')[-1].lstrip('0')
        if len(str) <= 1:
            return 'manual correction needed'
        if str[-1].isalpha() and str[-1] not in ['b', 'B']:
            str = str[:-1]

    elif str.count('-') > 1:
        return 'manual correction needed'

    return str

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
    data = pd.read_excel(args4main['input'])

    data.columns = data.columns.str.lower().str.strip().str.replace(" ", "_")
    cols = []
    warning_msg = ''
    for col_index, col_name in enumerate(data.columns):
        cols.append(col_name)

        if col_index >= 2 and col_index <= 20:
            data[col_name] = data[col_name].astype("string")
            data[col_name + '_standard'] = data[col_name]

            for row_index, value in data[col_name].items():
                if pd.notna(value):
                    match_pattern1 = re.search(
                        '(\d{2,4}-\d{1,2}-\d{1,2})', value)
                    match_pattern2 = re.search(
                        '(\d{1,2}/\d{1,2}/\d{2,4})', value)
                    if match_pattern1:
                        data[col_name +
                             '_standard'][row_index] = match_pattern1.group(1)
                        new_date = datetime.strptime(match_pattern1.group(
                            1), '%Y-%m-%d').strftime('%m/%d/%Y')
                        data[col_name][row_index] = new_date
                    elif match_pattern2:
                        data[col_name +
                             '_standard'][row_index] = match_pattern2.group(1)
                    else:
                        data[col_name + '_standard'][row_index] = np.nan
                        warning_msg += 'warning: A special char \'{}\' found at [row \'{}\', column \'{}\', pid \'{}\'] \n'.format(
                            value, row_index+2, col_name, data['pt.'][row_index])
                else:
                    data[col_name + '_standard'][row_index] = np.nan

            data[col_name +
                 '_standard'] = pd.to_datetime(data[col_name + '_standard']).dt.date
            data[col_name + '_days_from_baseline'] = (
                (data[col_name + '_standard'] - data['baseline_standard'])).dt.days

            cols.append(col_name + '_standard')
            cols.append(col_name + '_days_from_baseline')

    data = data[cols]

    ### reformat dataframe ###
    # create colums
    patient_id, root_tree, pid, timepoint_std, days, weeks, months, patient_initial, pid_raw, date_raw, date_std, timepoint_raw = ([
    ] for i in range(12))

    # iterate by row
    for index, row in data.iterrows():
        # skip null value row
        if pd.isna(row['pt.']) and pd.isna(row['pt_initials']):
            continue

        # iterate by column
        col_index = 0
        root_tree_count = 1
        for col_name, value in row.items():
            # from column 'baseline' to column '42_months'
            if col_index >= 2 and col_index <= 58:
                if 'standard' in col_name:
                    date_std.append(value)
                elif 'days' in col_name:
                    if value < 0:
                        days.append('manual correction needed (negative date duration)')
                        weeks.append('manual correction needed (negative date duration)')
                        months.append('manual correction needed (negative date duration)')
                        timepoint_std.append('manual correction needed (negative date duration)')
                    else:
                        days.append(value)
                        weeks.append(round(value/7, 1))
                        months.append(round(value/30, 1))
                        timepoint_std.append(find_closest_time(value))
                else:
                    patient_initial.append(row['pt_initials'])
                    date_raw.append(value)
                    timepoint_raw.append(col_name)
                    if pd.isna(row['pt.']):
                        pid_raw.append('manual correction needed')
                    else:
                        pid_raw.append(row['pt.'])

                    cur_pid = pid_extractor(str(row['pt.']))
                    pid.append(cur_pid)
                    cur_pat_id = cur_pid if cur_pid == 'manual correction needed' else 'IC_1_' + \
                        pid_extractor(str(row['pt.']))
                    patient_id.append(cur_pat_id)

                    cur_tree = 'IC_1_' + pid_extractor(str(row['pt.'])) + 'N'
                    if col_name == 'baseline':
                        root_tree.append(cur_tree)
                    else:
                        root_tree.append(cur_tree + str(root_tree_count))
                        root_tree_count += 1
                    if cur_pid == 'manual correction needed':
                        root_tree.pop()
                        root_tree.append('manual correction needed')

            col_index += 1

    df = {'patient_id': patient_id, 'root_tree': root_tree, 'pid': pid, 'timepoint_std': timepoint_std, 'days': days, 'weeks': weeks, 'months': months,
          'patient_initial': patient_initial, 'pid_raw': pid_raw, 'timepoint_raw': timepoint_raw, 'date_raw': date_raw, 'date_std': date_std}
    output = pd.DataFrame(data=df)

    output = output[(pd.isna(output['date_raw']) == False)]

    # pre-proccessed table
    data.to_csv('pre_output.csv', index=False, na_rep='NULL')
    # mid-output table
    output.to_csv('mid_output.csv', index=False, na_rep='NULL')

    with open('warning_msg.txt', "w") as f:
        if warning_msg:
            print(warning_msg, file=f)
        else:
            print('Success. No special chars found.', file=f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str,)

    args = parser.parse_args()

    args4main = {
        'input': args.input.strip(),
    }

    main(args4main)
