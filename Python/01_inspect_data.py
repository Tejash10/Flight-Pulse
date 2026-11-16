import pandas as pd

# ==========================================
# FLIGHT PULSE - DATASET INSPECTION
# ==========================================

# Load the flight dataset
df = pd.read_csv("Data/flight_delay.csv")


# 1. FIRST 5 ROWS
print("\n========== FIRST 5 ROWS ==========")
print(df.head())


# 2. DATASET SIZE
print("\n========== DATASET SIZE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# 3. COLUMN NAMES
print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print(column)


# 4. DATA TYPES
print("\n========== DATA TYPES ==========")
print(df.dtypes)


# 5. MISSING VALUES
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# 6. DUPLICATE ROWS
print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())


# 7. BASIC STATISTICS
print("\n========== BASIC STATISTICS ==========")
print(df.describe())


# 8. UNIQUE VALUES
print("\n========== UNIQUE VALUES ==========")
print(df.nunique())


print("\n========== INSPECTION COMPLETE ==========")