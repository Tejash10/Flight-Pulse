import pandas as pd

# ==========================================
# FLIGHT PULSE - PREPARE SQL DATA
# ==========================================

print("\n========================================")
print("     PREPARING DATA FOR MYSQL")
print("========================================")

# ==========================================
# 1. LOAD CLEAN DATASET
# ==========================================

print("\nLoading flights_clean.csv...")

df = pd.read_csv(
    r"D:\Flight_Pulse\Data\flights_clean.csv",
    low_memory=False
)

print("Rows loaded:", len(df))
print("Columns loaded:", len(df.columns))


# ==========================================
# 2. SELECT USEFUL SQL COLUMNS
# ==========================================

sql_columns = [
    "FLIGHT_DATE",
    "YEAR",
    "MONTH",
    "DAY",
    "DAY_OF_WEEK",
    "AIRLINE",
    "FLIGHT_NUMBER",
    "ORIGIN_AIRPORT",
    "DESTINATION_AIRPORT",
    "ROUTE",
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
    "DELAY_STATUS",
    "DELAY_CATEGORY",
    "DEPARTURE_HOUR",
    "AIR_SYSTEM_DELAY",
    "SECURITY_DELAY",
    "AIRLINE_DELAY",
    "LATE_AIRCRAFT_DELAY",
    "WEATHER_DELAY"
]

# Keep only columns that actually exist
available_columns = [
    column for column in sql_columns
    if column in df.columns
]

missing_columns = [
    column for column in sql_columns
    if column not in df.columns
]

df = df[available_columns].copy()

print("\nSelected columns:", len(df.columns))

if missing_columns:
    print("\nColumns not found:")
    print(missing_columns)


# ==========================================
# 3. CLEAN TEXT COLUMNS
# ==========================================

text_columns = [
    "AIRLINE",
    "ORIGIN_AIRPORT",
    "DESTINATION_AIRPORT",
    "ROUTE",
    "DELAY_STATUS",
    "DELAY_CATEGORY"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
        )


# ==========================================
# 4. CLEAN DATE
# ==========================================

if "FLIGHT_DATE" in df.columns:

    df["FLIGHT_DATE"] = pd.to_datetime(
        df["FLIGHT_DATE"],
        errors="coerce"
    )

    df["FLIGHT_DATE"] = (
        df["FLIGHT_DATE"]
        .dt.strftime("%Y-%m-%d")
    )


# ==========================================
# 5. REMOVE DUPLICATES
# ==========================================

before = len(df)

df = df.drop_duplicates().copy()

removed = before - len(df)

print("\nDuplicate rows removed:", removed)


# ==========================================
# 6. SAVE SQL DATASET
# ==========================================

output_path = (
    r"D:\Flight_Pulse\Data\flights_sql.csv"
)

print("\nSaving SQL-ready dataset...")

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 7. FINAL REPORT
# ==========================================

print("\n========================================")
print("       SQL DATASET READY")
print("========================================")

print("Final rows:", len(df))
print("Final columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nSaved to:")
print(output_path)

print("\n========================================")
print("          STEP 6A COMPLETE")
print("========================================")