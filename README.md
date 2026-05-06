# Cross-site Scripting (XSS) Detection System

a machine learning-based binary classification system using Random Forest to detect Cross-site Scripting (XSS) attacks.

## Overview

This project detects Cross-site Scripting attacks by grouping all attack types into two labels:
- **Cross-site Scripting (XSS)**
- **Other** (all non-XSS attack types)

The model uses numeric attack characteristics to distinguish XSS from other threats.

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

## Installation

### 1. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Dataset Format

Your CSV dataset should have the following columns:
- `Attack_ID`: Unique identifier for the attack record
- `Attack_Type`: Type of cyber attack (required for classification)
- `Target_Industry`: Industry targeted by the attack
- `Location`: Geographic location of the attack
- `Date`: Date of the attack
- `Severity`: Severity level of the attack (numeric)
- `Damage_Estimate(USD)`: Estimated financial damage in USD
- `Affected_Systems`: Number of affected systems

### Example Dataset Structure

```
Attack_ID,Attack_Type,Target_Industry,Location,Date,Severity,Damage_Estimate(USD),Affected_Systems
1,SQL Injection,Finance,USA,2023-01-15,8,500000,150
2,DDoS,Healthcare,UK,2023-01-16,9,2000000,500
3,Phishing,Retail,Canada,2023-01-17,5,100000,50
```

## Usage

### Basic Usage

Run the script with the default dataset name:

```bash
python csrf_detection.py
```

This will look for `cyber_attacks_dataset.csv` in the current directory.

### Using a Custom Dataset

Pass your dataset filename as an argument:

```bash
python csrf_detection.py your_dataset.csv
```

## Output

The script generates the following outputs:

1. **Console Output:**
   - Class distribution of the dataset
   - Training set and test set sizes
   - Classification report

2. **Saved files:**
   - `confusion_matrix.png`
   - `feature_importances.png`

