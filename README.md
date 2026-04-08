# Data Concatenation Transformer

## Purpose
Transforms Excel data by consolidating rows with the same `PartNumber` and `CompanyName` into single rows with feature data concatenated using "|" delimiter.

## How It Works - Detailed Function

### Core Transformation Logic

1. **Read Input Data**
   - Uses `pandas.read_excel()` with `keep_default_na=False` and `na_values=['']`
   - This preserves explicit "N/A" text while treating truly blank cells as NaN

2. **Group Data**
   - Groups rows by unique combination of `PartNumber` + `CompanyName`
   - All rows with same PartNumber and CompanyName are grouped together

3. **Process Each Group**
   - For each group, creates a single output row
   - Each feature row from the original data becomes a Feature column
   - Feature columns are named: Feature1, Feature2, Feature3, etc.

4. **Concatenate Values**
   - For each row in a group, extracts values from columns:
     - ZFeatureName
     - Value
     - ApprovalStatus
     - IsBackup
     - CorrectValue
     - SourceURL
     - Comment
     - Note
   - **Blank cells (NaN/empty)**: Skipped entirely (no || in output)
   - **Explicit "N/A" text**: Preserved as-is
   - **Other values**: Preserved exactly as they appear
   - Joins all values with " | " delimiter

5. **Generate Output**
   - Creates new Excel file with timestamp in filename
   - Format: `sample_format_[originalname]_[YYYYMMDD_HHMMSS].xlsx`
   - Preserves original file (no overwriting)

### Data Handling - N/A vs Blank Distinction

| Source Cell | How It's Treated | Output |
|-------------|------------------|--------|
| Truly blank/empty | Skipped | Not included in concatenation |
| Explicit "N/A" text | Preserved as-is | "N/A" appears in output |
| Actual value | Preserved as-is | Value appears in output |

### Why `keep_default_na=False`?

Standard pandas behavior converts these strings to NaN:
- "N/A", "NA", "NULL", "n/a", "na", "null"

With `keep_default_na=False`:
- "N/A" stays as the text string "N/A"
- Only truly empty cells become NaN
- This allows proper distinction between blank and N/A

## Files
- **`concat_transformer.py`** - The transformation tool
- **`sample output.xlsx`** - Template showing desired output format
- **`sample_format_...xlsx`** - Your transformed output files (with timestamps)

## Quick Start

### Run the Tool
```bash
python concat_transformer.py
```

The tool will:
1. Find Excel files in the current directory
2. Transform the data using concatenation method
3. Create output file with timestamp (no overwriting)

## Input Requirements
Your Excel file must contain:
- `PartNumber` column
- `CompanyName` column  
- Feature columns: `ZFeatureName`, `Value`, `ApprovalStatus`, `IsBackup`, `CorrectValue`, `SourceURL`, `Comment`, `Note`

## Output Format
The transformed file will have:
- `PartNumber` and `CompanyName` columns
- `Feature1`, `Feature2`, `Feature3`, etc. columns (one per original feature row)
- Each Feature column contains concatenated data with " | "

## Example Transformation

### Before (Multiple Rows):
| PartNumber | CompanyName | ZFeatureName | Value | ApprovalStatus | IsBackup |
|------------|-------------|--------------|-------|----------------|----------|
| ABC123     | Company A   | Voltage      | 5V    | Approved       |          |
| ABC123     | Company A   | Current      | 1A    | N/A            |          |
| ABC123     | Company A   | Power        | 5W    | Approved       | Yes      |

### After (Single Row):
| PartNumber | CompanyName | Feature1 | Feature2 | Feature3 |
|------------|-------------|----------|----------|----------|
| ABC123     | Company A   | Voltage \| 5V \| Approved | Current \| 1A \| N/A | Power \| 5W \| Approved \| Yes |

**Notice:**
- Blank IsBackup cells are skipped (no || in Feature1)
- Explicit "N/A" in ApprovalStatus is preserved (shown in Feature2)
- All actual values are concatenated with " | "

## Requirements
- Python 3.11+
- Packages: pandas, openpyxl

## Installation
```bash
# Install Python (if not already installed)
winget install Python.Python.3.11

# Install required packages
python -m pip install pandas openpyxl
```

## Usage
1. Place your Excel file in the same directory as `concat_transformer.py`
2. Run: `python concat_transformer.py`
3. Check the new output file with timestamp in filename

## Performance
- Fast processing for files of any size
- Automatic grouping by PartNumber+CompanyName
- Efficient concatenation with "|" delimiter
- Each run creates new file (no data loss)
