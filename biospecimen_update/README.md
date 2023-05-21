# Biospecimen Update

## Introduction

This script is to update time duration columns and the 'system_patient_id' column in *biospecimen.csv* file.

## Required Dependencies

The requirements dependencies are list below:

- Python = 3.7
- Pandas = 1.3.5

## Run This Script

Step 1: Build your enviroment (optional)

    conda create -n your_enviroment_name python=3.7
    conda activate your_enviroment_name
    pip install pandas=1.3.5

Step 2: Run update.py

    python update.py --input INPUT_FILE--output OUTPUT_FOLDER

This running will generate a *biospecimen_updated.csv* file under output folder.

## User Guideline

### command parameteres

Parameter | Description
---------------------------------------- | -------------
--input | The absolute or relative path of the input file. <br> e.g. /your_path/biospecimen.csv
--output | The absolute or relative path of the output folder. <br> e.g. /your_path/output_record

