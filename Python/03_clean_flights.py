import pandas as pd

# ==========================================
# FLIGHT PULSE - CLEAN FLIGHT DATA
# ==========================================

print("\n========================================")
print("      FLIGHT PULSE DATA CLEANING")
print("========================================")

# ==========================================
# 1. LOAD RAW DATASET
# ==========================================

print("\nLoading flights.csv...")

df = pd.read_csv(
    r"D:\Flight_Pulse\Data\flights.csv",
    low_memory=False
)

print("Dataset loaded successfully.")
print("Original rows:", len(df))
print("Original columns:", len(df.columns))


# ==========================================
# 2. SELECT USEFUL COLUMNS
# ==========================================

columns_to_keep = [
    "YEAR",
    "MONTH",
    "DAY",
    "DAY_OF_WEEK",
    "AIRLINE",
    "FLIGHT_NUMBER",
    "ORIGIN_AIRPORT",
    "DESTINATION_AIRPORT",
    "SCHEDULED_DEPARTURE",
    "DEPARTURE_TIME",
    "DEPARTURE_DELAY",
    "SCHEDULED_TIME",
    "ELAPSED_TIME",
    "AIR_TIME",
    "DISTANCE",
    "SCHEDULED_ARRIVAL",
    "ARRIVAL_TIME",
    "ARRIVAL_DELAY",
    "DIVERTED",
    "CANCELLED",
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

df = df[columns_to_keep].copy()

print("\nUseful columns selected.")


# ==========================================
# 3. CONVERT NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "YEAR",
    "MONTH",
    "DAY",
    "DAY_OF_WEEK",
    "FLIGHT_NUMBER",
    "SCHEDULED_DEPARTURE",
    "DEPARTURE_TIME",
    "DEPARTURE_DELAY",
    "SCHEDULED_TIME",
    "ELAPSED_TIME",
    "AIR_TIME",
    "DISTANCE",
    "SCHEDULED_ARRIVAL",
    "ARRIVAL_TIME",
    "ARRIVAL_DELAY",
    "DIVERTED",
    "CANCELLED",
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("Numeric columns converted.")


# ==========================================
# 4. CLEAN AIRPORT COLUMNS
# ==========================================

df["ORIGIN_AIRPORT"] = (
    df["ORIGIN_AIRPORT"]
    .fillna("UNKNOWN")
    .astype(str)
    .str.strip()
)

df["DESTINATION_AIRPORT"] = (
    df["DESTINATION_AIRPORT"]
    .fillna("UNKNOWN")
    .astype(str)
    .str.strip()
)

print("Airport columns cleaned.")


# ==========================================
# 5. REMOVE CANCELLED FLIGHTS
# ==========================================

before_cancelled = len(df)

df = df[df["CANCELLED"] == 0].copy()

print(
    "Cancelled flights removed:",
    before_cancelled - len(df)
)


# ==========================================
# 6. REMOVE DIVERTED FLIGHTS
# ==========================================

before_diverted = len(df)

df = df[df["DIVERTED"] == 0].copy()

print(
    "Diverted flights removed:",
    before_diverted - len(df)
)


# ==========================================
# 7. REMOVE MISSING DEPARTURE DELAYS
# ==========================================

before_missing = len(df)

df = df.dropna(
    subset=["DEPARTURE_DELAY"]
).copy()

print(
    "Rows without departure delay removed:",
    before_missing - len(df)
)


# ==========================================
# 8. CREATE DELAY STATUS
# ==========================================

df["DELAY_STATUS"] = df["DEPARTURE_DELAY"].apply(
    lambda x: "Delayed" if x > 15 else "On Time"
)


# ==========================================
# 9. CREATE DELAY CATEGORY
# ==========================================

def delay_category(minutes):

    if minutes <= 15:
        return "On Time"

    elif minutes <= 30:
        return "Minor Delay"

    elif minutes <= 60:
        return "Moderate Delay"

    elif minutes <= 120:
        return "Major Delay"

    else:
        return "Severe Delay"


df["DELAY_CATEGORY"] = (
    df["DEPARTURE_DELAY"]
    .apply(delay_category)
)


# ==========================================
# 10. CREATE FLIGHT DATE
# ==========================================

df["FLIGHT_DATE"] = pd.to_datetime(
    {
        "year": df["YEAR"],
        "month": df["MONTH"],
        "day": df["DAY"]
    },
    errors="coerce"
)


# ==========================================
# 11. CREATE DEPARTURE HOUR
# ==========================================

df["DEPARTURE_HOUR"] = (
    df["SCHEDULED_DEPARTURE"] // 100
)

# Make sure the value is between 0 and 23
df["DEPARTURE_HOUR"] = (
    df["DEPARTURE_HOUR"]
    .clip(lower=0, upper=23)
)


# ==========================================
# 12. CREATE ROUTE
# ==========================================

df["ROUTE"] = (
    df["ORIGIN_AIRPORT"]
    + " → "
    + df["DESTINATION_AIRPORT"]
)


# ==========================================
# 13. REMOVE DUPLICATES
# ==========================================

before_duplicates = len(df)

df = df.drop_duplicates().copy()

print(
    "Duplicate rows removed:",
    before_duplicates - len(df)
)


# ==========================================
# 14. SORT DATA
# ==========================================

df = df.sort_values(
    by="FLIGHT_DATE"
)


# ==========================================
# 15. SAVE CLEAN DATASET
# ==========================================

output_path = (
    r"D:\Flight_Pulse\Data\flights_clean.csv"
)

print("\nSaving cleaned dataset...")

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 16. FINAL REPORT
# ==========================================

print("\n========================================")
print("       CLEANING COMPLETE")
print("========================================")

print("\nFinal rows:", len(df))
print("Final columns:", len(df.columns))

print("\nDelay Status:")
print(
    df["DELAY_STATUS"].value_counts()
)

print("\nDelay Categories:")
print(
    df["DELAY_CATEGORY"].value_counts()
)

print("\nRemaining missing values:")
print(
    df.isnull().sum()
)

print("\nSaved file:")
print(output_path)

print("\n========================================")
print("       FLIGHT PULSE READY")
print("========================================")