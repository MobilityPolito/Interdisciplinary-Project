#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:07:56 2016

@author: alecioc
"""

import os
import pandas as pd

datasource_dirs = ["torino_it", "enjoy", "car2go" ]
datasource_dict = { k:[] for k in datasource_dirs }

rawdata_path = "./RawData/"
cleandata_path = "./CleanData/"

def clean_files ():
    for ds_dir in datasource_dirs:
    
        input_dir = rawdata_path + ds_dir + "/"
        if not os.path.exists(cleandata_path):
            os.makedirs(cleandata_path)
        output_dir = cleandata_path + ds_dir + "/"
    
        if ds_dir == "torino_it":
            for filename in sorted(os.listdir(input_dir)):
                datasource_dict[ds_dir].append(filename)
                df = pd.read_csv(input_dir + filename)
                if df.isnull().values.any():
                    for col in df:
                        mask = df[col].isnull()
                        if len(mask[mask == True]) == len(df[col]):
                            df.drop(col, axis=1, inplace=True)
                with open(output_dir + filename, 'w+') as output_file:
                    df.to_csv(output_file)
                
def load (datasource, filename):
    return pd.read_csv(cleandata_path + datasource + "/" + filename)
    
clean_files()