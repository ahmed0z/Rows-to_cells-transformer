# Data Transformer - Streamlit App

A modern web application for transforming Excel data by consolidating rows with the same PartNumber and CompanyName into single rows with concatenated feature data.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL_HERE)

## 📋 Features

### Concatenate Data
- **Groups** rows by PartNumber + CompanyName
- **Concatenates** feature data with "|" delimiter
- **Skips** blank cells (no empty || in output)
- **Preserves** explicit "N/A" text as-is
- **Analysis dashboard** showing unique parts, feature counts, and distributions

### Reverse Transformation
- **Splits** concatenated data back to original format
- **Restores** original column structure
- **Multiple rows** per PartNumber
- **Data integrity** fully preserved

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **Data Processing**: NumPy, OpenPyXL
- **Styling**: Custom CSS with modern UI

## 📦 Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/data-transformer.git
cd data-transformer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Requirements
- Python 3.11+
- Streamlit 1.28+
- Pandas 2.0+
- OpenPyXL 3.1+

## 🎯 Usage

1. **Upload** your Excel file (must have PartNumber and CompanyName columns)
2. **View** the data analysis dashboard
3. **Transform** the data with one click
4. **Download** the result

## 📊 Input Format

Your Excel file should have:
- `PartNumber` column
- `CompanyName` column
- Feature columns: `ZFeatureName`, `Value`, `ApprovalStatus`, `IsBackup`, `CorrectValue`, `SourceURL`, `Comment`, `Note`

## 🔄 Transformation Logic

### Concatenation
```
Before:                    After:
PartNumber | CompanyName   PartNumber | CompanyName | Feature1
ABC123     | Company A     ABC123     | Company A   | Voltage | 5V | Approved
ABC123     | Company A                                   | Current | 1A | Approved
```

### Reverse
```
Input:                     Output:
PartNumber | Feature1      PartNumber | CompanyName | ZFeatureName | Value
ABC123     | Voltage|5V   ABC123     | Company A   | Voltage      | 5V
```

## 🌟 Key Features

- ✅ Modern, responsive UI
- ✅ Real-time data analysis
- ✅ Interactive charts
- ✅ Progress indicators
- ✅ Download functionality
- ✅ No data loss
- ✅ N/A vs Blank distinction

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit**
