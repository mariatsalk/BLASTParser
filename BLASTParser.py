#!/usr/bin/python3
"""
Title: BINP28 - Exercise: BLAST parser

Date: 24/01/2022

Author(s): Maria Tsalkitzidou


Description:
    The script takes as input a default BLAST output file and parses it. As it parses it holds only the wanted information and creates a tab delimited file with 5 columns consisting it. The first column is the query name, the second is the targer, the third columns is the e-value, the fourth column is the identity score and the fifth column is the score. In the case of mutliple hits it prints them all.

List of functions:
    No functions were used

List of modules:
    1. argparse
    2. re
    3. os

List of bugs:
    1. If no specific name is given for the output file and the default_output_file.tsv already exists it will be overwritten.
    2. The script does not check if the input file is in the appropriate format. 

Procedure:
    1. Import the necessary modules.
    2. Load the file and create the necessary variables.
    3. Iterate through the blastp file and search for the queries. The information is stored in a dictionary with the query id and the hit sequence id as keys and the rest of information as value.
    4. When a query is found the script searches if it has hits or not. If it has no hits it adds empty strings in the dictionary. If it has hits it adds the information in the appropriate position in the dictionary.
    5. The results are written in a file.


Usage: python BLASTParser.py -i input_file -o output_file

"""
#%% Importing packages

import argparse
import re
import os

#%% Importing the file from the terminal

parser = argparse.ArgumentParser()
usage ='Parses a blastp file and outputs a file that contains specific information for every query'
parser.add_argument(
    '-i', 
    '--input_file', 
    required=True, 
    help='The input file, with your NCBI BLASTp data'
    )
parser.add_argument(
    '-o', 
    '--output_file', 
    required=False, 
    default='default_output_file', 
    help='Tab separated file to output the results from your data'
    )
args=parser.parse_args()

#%% Reading the input file and converting the output

# Checking if the input file is empty and if it is raise exception
if os.stat(args.input_file).st_size == 0:
    raise Exception("The input file should not be empty")

#Check if all the mandatory information is passed
if args.input_file:
    
    # Open the input and output files
    in_file=open(args.input_file, 'r')
    out_file=open('{}.tsv'.format(args.output_file), 'w')
        
    
    #make the necessary variables
    final_table = {} #Empty dictionary to store all the output
    no_hit = ['']*3 #A list with empty strings for the queries with no hits
    
    
    for line in in_file: #Iterate through the file line to line
    
        if line.startswith('Query='): #Found a query
            query = line.rstrip().split()[1] #Keep only the id of the query
    
        elif line.startswith('***** No hits found *****'): #There are no hits for this query
            query_no_hit= query + "\t" + '' #Combine the query id with an empty string in order to keep the same format as in the case of finding a hit sequence
            final_table[query_no_hit]=no_hit #Assing the empty strings to the query
    
        elif line.startswith('>'): #There are hits for this query
            target = line.rstrip().split('>')[1] #Keep only the sequence id of the hit
    
            query_target= query + "\t" + target #Combine the query id and the sequence id to avoid overwritting information when we have multiple hits for one query
            final_table[query_target]=['']*3 #Assign the combined query id and sequence id as key to the dictionary and empty strings as values
    
            #Skip the next two lines in order to get to the blast statistics
            next(in_file)
            next(in_file)
    
            line1=next(in_file) #Line 1 of the blast statistics
            line1=re.sub('[,()]','', line1) #Remove unwanted characters
            evalue = line1.rstrip().split()[7] #Extract the e-value from the line and store it to a temporary variable
            score = line1.rstrip().split()[4] #Extract the score from the line and store it to a temporary variable
            final_table[query_target][0] = evalue #Add the e-value in the dictionary in the correct position
            final_table[query_target][2] = score #Add the score in the dictionary in the correct position
            line2=next(in_file) #Move to line 2 of the blast statistics
            line2=re.sub('[,()%]','',line2) #Remove unwanted characters
            identity = line2.rstrip().split()[3] #Extract the identity % from th line and store it to a temporary variable
            final_table[query_target][1] = identity #Add the identity in the dictionary in the correct position
    
    
    #print(final_table) #Checkpoint
    
    #Print the header in the file
    out_file.write("#query" + "\t" + "target" + "\t" + "e-value" + "\t" + "identity(%)" + "\t" + "score" + "\n")
    
    #Print the final results in the output file
    for k in final_table:
        out_file.write('{}\t{}\t{}\t{}\n'.format(k, final_table[k][0], final_table[k][1], final_table[k][2]))
    
    
    #Close the files
    in_file.close()
    out_file.close()
    
else:
    raise Exception('The provided input file does not exist. Please try again!')