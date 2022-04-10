# BLASTParser

Current Version: 1.0

## About the program

BLASTParser is a parser for NCBI BLASTp results. It parses through the file and creates a new output file containing selected categories of information for each query sequence. Specifically the query sequence name, the target sequence name, the e-value of the match, the identity percent of the match, and the match score.



### Running the program

There are various options when running the program via the command line, depending on what the user wants to achieve. To read about the options of the program simply run:

```bash
python BLASTParser.py --help
```

Flag options:
- -i or --input_file: The NCBI BLASTp results file.
- -o or --output_file: creates a tsv file with the tab-separated table containing the selected information. As argument it takes the desired file name.


The -o --output_file flag optional. If no argument is provided the script will generate a file called default_output_file.tsv

The -i --input_file flag is mandatory.


An example run would look like this, using one of the example sequences and their motif:

 ```bash
 python BLASTParser.py -i example_input_file.blastp -o example_output_file
 ```

## Results

The output file will contain a tab-separated table organized in the following manner:
 - Header line: the query sequence name, the target sequence name, the e-value of the match, the identity percent of the match, and the match score.
 - Results lines: The results from the BLASTp organized according to the columns labeled in the header. Query sequences without BLASTp hits will still appear in the query column, but the rest of the row will be blank.
