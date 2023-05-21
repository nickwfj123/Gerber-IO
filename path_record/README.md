# File Names and Paths Record

## Introduction

This script is to extract name, absolute path and type of each file and record them in a csv output file.

## Required Dependencies

The requirements dependencies are list below:

- Python = 3.7
- Pandas = 1.3.5

## Run This Script

Step 1: Build your enviroment (optional)

    conda create -n your_enviroment_name python=3.7
    conda activate your_enviroment_name
    pip install pandas=1.3.5

Step 2: Run recorder.py

    python recorder.py --input INPUT_FOLDER --output OUTPUT_FOLDER --type FILE_TYPE

This running will generate a result.csv file under output folder.

## User Guideline

### command parameteres

Parameter | Description
---------------------------------------- | -------------
--input | The absolute or relative path of input folder. <br> e.g. /your_path/Helios-Gerber_UO1
--output | The absolute or relative path of output folder. <br> e.g. /your_path/output_record
--type (optional) | The file type you want to extract. <br> e.g. fcs, txt, pdf, csv. <br> (By default, it will extract all types.)
