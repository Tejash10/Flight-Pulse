import pandas as pd

# ==========================================
# FLIGHT PULSE - REFERENCE DATA INSPECTION
# ==========================================

# Load airline data
airlines = pd.read_csv(
    r"D:\Flight_Pulse\Data\airlines.csv"
)

# Load airport data
airports = pd.read_csv(
    r"D:\Flight_Pulse\Data\airports.csv"
)


# ==========================================
# AIRLINES
# ==========================================

print("\n========================================")
print("             AIRLINES")
print("========================================")

print("\nRows:", len(airlines))
print("Columns:", len(airlines.columns))

print("\nColumn names:")
print(airlines.columns.tolist())

print("\nFirst 5 rows:")
print(airlines.head())

print("\nMissing values:")
print(airlines.isnull().sum())


# ==========================================
# AIRPORTS
# ==========================================

print("\n========================================")
print("             AIRPORTS")
print("========================================")

print("\nRows:", len(airports))
print("Columns:", len(airports.columns))

print("\nColumn names:")
print(airports.columns.tolist())

print("\nFirst 5 rows:")
print(airports.head())

print("\nMissing values:")
print(airports.isnull().sum())


print("\n========================================")
print("       INSPECTION COMPLETE")
print("========================================")