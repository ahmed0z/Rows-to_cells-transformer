#!/usr/bin/env python3
"""
Concatenating Data Transformer Tool
Transforms Excel data by consolidating rows with the same PartNumber and CompanyName
and concatenating feature data with | delimiter into single cells.
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import sys
import os
from pathlib import Path
import time

def examine_excel_file(file_path):
    """Examine the structure of an Excel file"""
    try:
        print(f"Reading file structure...")
        df = pd.read_excel(file_path, nrows=5)
        print(f"File: {file_path}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Get actual row count
        df_full = pd.read_excel(file_path)
        print(f"\nTotal rows: {len(df_full)}")
        print(f"Total columns: {len(df.columns)}")
        
        return df_full
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def create_sample_output_format(input_file, output_file):
    """
    Create output with the format from sample output.xlsx
    """
    try:
        print("Creating output in sample format...")
        
        # Read input data with keep_default_na=False to preserve N/A strings
        # Only treat empty strings as NaN/blank, not "N/A" text values
        df = pd.read_excel(input_file, keep_default_na=False, na_values=[''])
        
        # Group by PartNumber and CompanyName
        grouped = df.groupby(['PartNumber', 'CompanyName'])
        
        transformed_rows = []
        
        for (part_num, company), group in grouped:
            row_data = {
                'PartNumber': part_num,
                'CompanyName': company
            }
            
            # Create feature columns by concatenating all data for each row
            feature_columns = []
            
            for idx, (_, feature_row) in enumerate(group.iterrows()):
                # Concatenate all feature data for this row - SKIP BLANK CELLS
                feature_data_parts = []
                for col in ['ZFeatureName', 'Value', 'ApprovalStatus', 'IsBackup', 'CorrectValue', 'SourceURL', 'Comment', 'Note']:
                    value = feature_row.get(col, '')
                    # With keep_default_na=False:
                    # - NaN = truly blank/empty cell (skip these)
                    # - "N/A" = explicit N/A text (preserve as-is)
                    # - Other values = preserved as-is
                    if pd.isna(value):
                        # Truly blank/empty cell - skip it (don't add to parts)
                        continue
                    elif str(value).strip() == '':
                        # Empty string - skip it
                        continue
                    else:
                        # Has actual value (including explicit "N/A" text) - preserve exactly as-is
                        feature_data_parts.append(str(value))
                
                # Join with | delimiter (blank cells are now excluded)
                feature_data = ' | '.join(feature_data_parts)
                
                # Add as Feature1, Feature2, etc.
                feature_col_name = f'Feature{idx + 1}'
                row_data[feature_col_name] = feature_data
                feature_columns.append(feature_col_name)
            
            transformed_rows.append(row_data)
        
        # Create DataFrame
        transformed_df = pd.DataFrame(transformed_rows)
        
        # Fill missing feature columns with empty strings (blank) to preserve distinction from N/A
        max_features = max([len(row) - 2 for row in transformed_rows])  # Subtract PartNumber and CompanyName
        
        for i in range(1, max_features + 1):
            feature_col = f'Feature{i}'
            if feature_col not in transformed_df.columns:
                transformed_df[feature_col] = ''
        
        # Reorder columns to match sample format
        feature_cols = [f'Feature{i}' for i in range(1, max_features + 1)]
        column_order = ['PartNumber', 'CompanyName'] + feature_cols
        transformed_df = transformed_df[column_order]
        
        # Save to output file
        transformed_df.to_excel(output_file, index=False)
        
        print(f"Sample format output saved to: {output_file}")
        print(f"Shape: {transformed_df.shape}")
        print(f"Columns: {list(transformed_df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"Error creating sample format: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the concatenating data transformer"""
    print("=== Concatenating Data Transformer Tool ===")
    
    # Get current directory
    current_dir = Path(__file__).parent
    print(f"Working directory: {current_dir}")
    
    # Find Excel files
    excel_files = list(current_dir.glob("*.xlsx"))
    excel_files = [f for f in excel_files if not f.name.startswith("~$")]
    
    if not excel_files:
        print("No Excel files found!")
        return
    
    print(f"\nFound Excel files:")
    for i, file in enumerate(excel_files, 1):
        print(f"{i}. {file.name} ({file.stat().st_size / 1024:.1f} KB)")
    
    # Select input file
    input_file = None
    for file in excel_files:
        if 'input' in file.name.lower():
            input_file = file
            break
    
    if not input_file:
        input_file = excel_files[0]
    
    print(f"\nUsing input file: {input_file.name}")
    print(f"File size: {input_file.stat().st_size / 1024:.1f} KB")
    
    # Examine file
    print("\n=== Examining Input File ===")
    df = examine_excel_file(input_file)
    
    if df is None:
        print("Could not read input file!")
        return
    
    # Create sample format output (the chosen format)
    print("\n=== Creating Sample Format Output ===")
    
    # Add timestamp to filename to avoid overwriting existing file
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = current_dir / f"sample_format_{input_file.stem}_{timestamp}.xlsx"
    success = create_sample_output_format(input_file, output_file)
    
    if success:
        print(f"\n=== Transformation Complete ===")
        print(f"Output file: {output_file}")
        result_df = pd.read_excel(output_file)
        print(f"Shape: {result_df.shape}")
        print("\nFirst 3 rows:")
        print(result_df.head(3).to_string())
    else:
        print("Transformation failed!")

if __name__ == "__main__":
    main()
