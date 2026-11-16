import pandas as pd

# ==========================================
# FLIGHT PULSE - FLIGHTS DATASET INSPECTION
# ==========================================

# Load flights dataset
df = pd.read_csv(r"D:\Flight_Pulse\Data\flights.csv")


# Dataset size
print("\n========== DATASET SIZE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# Column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())


# First 5 rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head())


# Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)


# Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# Duplicate rows
print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())


print("\n========== INSPECTION COMPLETE ==========")