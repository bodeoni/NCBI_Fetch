# -*- coding: utf-8 -*-
!pip install pycountry

# Commented out IPython magic to ensure Python compatibility.
#Import libraries
import re
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import missingno as msn
import glob
import ast
import pycountry
# %matplotlib inline

# read in all the files and concatenate them
path = r'/content/drive/My Drive/Chinedu' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

data = pd.concat(li, axis=0, ignore_index=True)

print("Dataset has",data.shape[0], "rows and ",data.shape[1],"columns")

columns = data.columns.to_list()

columns

# Drop unwanted columns
drop = ['Unnamed: 0',
 'GBSeq_length',
 'GBSeq_strandedness',
 'GBSeq_accession-version',
 'GBSeq_other-seqids',
 'GBSeq_feature-table',
 'GBSeq_sequence',
 'GBSeq_comment',
 'GBSeq_project',
 'GBSeq_xrefs',
 'GBSeq_keywords',
 'GBSeq_alt-seq',
 'GBSeq_primary']

#save to new dataframe
data2= data.drop(drop, axis=1)

# Rename collumns
data2.columns = ['locus',
 'moltype',
 'topology',
 'division',
 'update-date',
 'create-date',
 'definition',
 'primary-accession',
 'source',
 'organism',
 'taxonomy',
 'references']

data2.info()

data2['taxonomy']= data2['taxonomy'].astype(str)
data2['taxonomy']= data2['taxonomy'].str.replace(';','')

# Functions to Extract taxonomies for GBseq_taxonomy columns
#Phylum
def phylum(x):
    items = re.findall(r'\b(\w+phyta)\b', x)
    if items == []:
        return np.nan
    else:
        return items[0]


#class
def class_1(x):
    items = re.findall(r'\b(\w+sida)\b', x)
    if items == []:
        return np.nan
    else:
        return items[0]


#order
def order(x):
    items = re.findall(r'\b(\w+ales)\b', x)
    if items == []:
        return np.nan
    else:
        return items[0]


#family
def family(x):
    items = re.findall(r'\b(\w+aceae)\b', x)
    if items == []:
        return np.nan
    else:
        return items[0]

    #Function to extract countries
def extract_countries(x):
    for country in pycountry.countries:
        if country.name in x:
            return(country.name)

#Create taxonmy columns
data2['phylum'] = data2['taxonomy'].apply(lambda x: phylum(x))
data2['class'] = data2['taxonomy'].apply(lambda x: class_1(x))
data2['order'] = data2['taxonomy'].apply(lambda x: order(x))
data2['family'] = data2['taxonomy'].apply(lambda x: family(x))
data2['genus'] = data2['organism'].str.split(' ', expand=True)[0]
data2['species'] = data2['organism'].str.split(' ', expand=True)[1]

data2['references'] = data2['references'].apply(ast.literal_eval)
data2['references'] = data2['references'].apply(lambda x: x[-1])
data2['references'] = data2['references'].apply(lambda x: x['GBReference_journal'])

data2['references']= data2['references'].str.replace('USA', 'United States')
data2['references']= data2['references'].str.replace('UK', 'United Kingdom')
data2['references']= data2['references'].str.title()

data2['Country']=data2['references'].apply(lambda x: extract_countries(x))

data2['Country'].value_counts().sum()

country_counts = data2['Country'].value_counts().rename_axis('countries').reset_index(name='counts')

data2.tail()

msn.matrix(data2)

drop=['locus','definition','source','organism','taxonomy','references','topology', 'update-date']
data3 = data2.drop(drop, axis=1)

data3['division'].value_counts()

data3 = data3[data3['moltype']=='DNA']
data3 = data3[data3['division']=='PLN']

data3 =data3.drop(['moltype','division'], axis=1)

data3.shape

final = data3

final.info()

msn.matrix(final)

final.to_csv('clean_data.csv')

