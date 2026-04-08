#!/usr/bin/env python3
"""
Reverse Data Transformer Tool
Transforms concatenated Excel data back to original format by splitting
Feature columns with "|" delimiter into separate rows.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def reverse_transform(input_file, output_file):
    """
    Reverse the concatenation transformation
    Takes file with Feature1, Feature2 columns and converts back to original format
    """
    try:
        print(f"Starting reverse transformation at {datetime.now().strftime('%H:%M:%S')}")
        
        # Read the concatenated file
        print("Reading input file...")
        df = pd.read_excel(input_file)
        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Check required columns
        required_cols = ['PartNumber', 'CompanyName']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Missing required columns: {missing_cols}")
            return False
        
        # Get Feature columns (everything after PartNumber and CompanyName)
        feature_cols = [col for col in df.columns if col not in required_cols]
        print(f"Feature columns found: {feature_cols}")
        
        # Original column order
        original_cols = ['PartNumber', 'CompanyName', 'ZFeatureName', 'Value', 
                        'ApprovalStatus', 'IsBackup', 'CorrectValue', 'SourceURL', 
                        'Comment', 'Note']
        
        reversed_rows = []
        
        # Process each row
        for idx, row in df.iterrows():
            part_num = row['PartNumber']
            company = row['CompanyName']
            
            # Process each Feature column
            for feature_col in feature_cols:
                feature_data = row.get(feature_col, '')
                
                # Skip if feature data is empty or NaN
                if pd.isna(feature_data) or str(feature_data).strip() == '':
                    continue
                
                # Split by " | " delimiter
                parts = str(feature_data).split(' | ')
                
                # Create new row with original format
                new_row = {
                    'PartNumber': part_num,
                    'CompanyName': company
                }
                
                # Map parts to original columns (skip PartNumber and CompanyName)
                # parts[0] -> ZFeatureName, parts[1] -> Value, etc.
                for i, col in enumerate(original_cols[2:]):  # Skip PartNumber, CompanyName
                    if i < len(parts):
                        value = parts[i].strip()
                        # Convert 'N/A' back to actual N/A text, empty stays empty
                        new_row[col] = value if value else None
                    else:
                        new_row[col] = None
                
                reversed_rows.append(new_row)
        
        # Create DataFrame with original column order
        reversed_df = pd.DataFrame(reversed_rows, columns=original_cols)
        
        print(f"Reverse transformation complete:")
        print(f"Input rows: {len(df)}")
        print(f"Output rows: {len(reversed_df)}")
        print(f"Columns: {list(reversed_df.columns)}")
        
        # Save to output file
        reversed_df.to_excel(output_file, index=False)
        print(f"Output saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error during reverse transformation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the reverse transformer"""
    print("=== Reverse Data Transformer Tool ===")
    print("Converts concatenated format back to original format")
    
    # Get current directory
    current_dir = Path(__file__).parent
    print(f"Working directory: {current_dir}")
    
    # Find Excel files (excluding temp files and original input files)
    excel_files = list(current_dir.glob("*.xlsx"))
    excel_files = [f for f in excel_files if not f.name.startswith("~$")]
    # Filter for sample_format files, exclude original input and reversed files
    excel_files = [f for f in excel_files if 
                   'sample_format' in f.name.lower() and 
                   'input' not in f.name.lower() and
                   'reversed' not in f.name.lower()]
    
    if not excel_files:
        print("No sample_format Excel files found!")
        print("Looking for files with 'sample_format' in the name...")
        return
    
    print(f"\nFound {len(excel_files)} sample_format file(s):")
    for i, file in enumerate(excel_files, 1):
        print(f"{i}. {file.name}")
    
    # Use the most recent file (last in list if sorted by name with timestamp)
    input_file = sorted(excel_files)[-1]  # Most recent by timestamp
    
    print(f"\nUsing input file: {input_file.name}")
    print(f"File size: {input_file.stat().st_size / 1024:.1f} KB")
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = current_dir / f"reversed_{input_file.stem}_{timestamp}.xlsx"
    
    # Run reverse transformation
    print("\n=== Starting Reverse Transformation ===")
    success = reverse_transform(input_file, output_file)
    
    if success:
        print(f"\n=== Reverse Transformation Complete ===")
        
        # Show sample of output
        result_df = pd.read_excel(output_file)
        print(f"\nFirst 5 rows of reversed data:")
        print(result_df.head().to_string())
        print(f"\nTotal rows restored: {len(result_df)}")
    else:
        print("Reverse transformation failed!")

if __name__ == "__main__":
    main()
