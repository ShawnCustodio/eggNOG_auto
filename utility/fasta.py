#!/usr/bin/env python3
# fasta_from_excel.py
# Usage: python fasta_from_excel.py input.xlsx header_column sequence_column output.faa

import sys
import pandas as pd

def excel_to_fasta(excel_file, header_col, sequence_col, output_fasta):
    # Load Excel
    df = pd.read_excel(excel_file)
    
    # Check columns exist
    if header_col not in df.columns or sequence_col not in df.columns:
        print(f"Error: columns '{header_col}' or '{sequence_col}' not found in {excel_file}")
        sys.exit(1)
    
    # Write FASTA
    with open(output_fasta, 'w') as f:
        for idx, row in df.iterrows():
            header = str(row[header_col])
            seq = str(row[sequence_col]).replace("\n","").replace("\r","")
            f.write(f">{header}\n{seq}\n")
    
    print(f"FASTA created: {output_fasta} ({len(df)} sequences)")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python fasta_from_excel.py input.xlsx header_column sequence_column output.faa")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    header_col = sys.argv[2]
    sequence_col = sys.argv[3]
    output_fasta = sys.argv[4]
    
    excel_to_fasta(excel_file, header_col, sequence_col, output_fasta)