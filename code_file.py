!pip install biopython

from Bio import Entrez
import pandas as pd
from google.colab import drive
drive.mount('/content/gdrive')

# Obtain fasta summaries

Entrez.email = "bodeoni@yahoo.com"  # Email

#Perform intial search using history and save results in file
search_handle = Entrez.esearch(db="nucleotide", term="(rbcl AND plants[filter] AND biomol_genomic[PROP] AND is_nuccore[filter])", 
                               usehistory="y", 
                               idtype="acc")
search_results = Entrez.read(search_handle)
search_handle.close()

acc_list = search_results["IdList"] #accession list
count = int(search_results["Count"]) #total number of record from query

print('Total number of records for your query is: ' + str(count))
#define web environment key and query key
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]

# Since NCBI only allows a maximum of 10000 downloads per time, do a for loop to download items in batches.
batch_size = 10000
num =1
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Now downloading records %i to %i" % (start+1, end))
    out_handle = open("batch.xml", "wb")
    fetch_handle = Entrez.efetch(db="nucleotide",
                                 rettype="gb", retmode="xml",
                                 retstart=start, retmax=end,
                                 webenv=webenv, query_key=query_key,
                                 idtype="acc", seq_start="1", seq_stop="1", complexity="2")
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
    out_handle.close()
    
    print("Now processing records %i to %i" % (start+1, end))
    
    handle = open("batch.xml", "rb")
    record_new= Entrez.read(handle, validate=False)

    link ='/content/gdrive/My Drive/gb_sum_'+ str(num) + '.csv'

    df =pd.DataFrame.from_dict(record_new, orient='columns')
    df.to_csv(link)
    num= num+1
    print("Done processing records %i to %i" % (start+1, end))
    print(" ")
print('Done')

# Obtain fasta summaries

Entrez.email = "bodeoni@yahoo.com"  # Email

#Perform intial search using history and save results in file
search_handle = Entrez.esearch(db="nucleotide", term="(rbcl AND plants[filter] AND biomol_genomic[PROP] AND is_nuccore[filter])", 
                               usehistory="y", 
                               idtype="acc")
search_results = Entrez.read(search_handle)
search_handle.close()

acc_list = search_results["IdList"] #accession list
count = int(search_results["Count"]) #total number of record from query

print('Total number of records for your query is: ' + str(count))
#define web environment key and query key
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]

# Since NCBI only allows a maximum of 10000 downloads per time, do a for loop to download items in batches.
batch_size = 10000
num =1
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Now downloading records %i to %i" % (start+1, end))
    out_handle = open("batch.xml", "wb")
    fetch_handle = Entrez.efetch(db="nucleotide",
                                 rettype="fasta", retmode="xml",
                                 retstart=start, retmax=end,
                                 webenv=webenv, query_key=query_key,
                                 idtype="acc", seq_start="1", seq_stop="1", complexity="2")
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
    out_handle.close()
    
    print("Now processing records %i to %i" % (start+1, end))
    
    handle = open("batch.xml", "rb")
    record_new= Entrez.read(handle, validate=False)

    link ='/content/gdrive/My Drive/fasta_sum_'+ str(num) + '.csv'

    df =pd.DataFrame.from_dict(record_new, orient='columns')
    df.to_csv(link)
    num= num+1
    print("Done processing records %i to %i" % (start+1, end))
    print(" ")
print('Done')
