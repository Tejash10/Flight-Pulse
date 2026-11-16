import pandas as pd

# ==========================================
# FLIGHT PULSE - BUILD FINAL DATASET
# ==========================================

print("\n========================================")
print("   BUILDING FLIGHT PULSE DATASET")
print("========================================")


# ==========================================
# 1. LOAD DATA
# ==========================================

print("\nLoading files...")

flights = pd.read_csv(
    r"D:\Flight_Pulse\Data\flights_clean.csv",
    low_memory=False
)

airlines = pd.read_csv(
    r"D:\Flight_Pulse\Data\airlines.csv",
    low_memory=False
)

airports = pd.read_csv(
    r"D:\Flight_Pulse\Data\airports.csv",
    low_memory=False
)

print("Flights:", len(flights))
print("Airlines:", len(airlines))
print("Airports:", len(airports))


# ==========================================
# 2. CLEAN COLUMN NAMES
# ==========================================

flights.columns = flights.columns.str.strip()
airlines.columns = airlines.columns.str.strip()
airports.columns = airports.columns.str.strip()


# ==========================================
# 3. CHECK REFERENCE COLUMNS
# ==========================================

print("\nAirline columns:")
print(airlines.columns.tolist())

print("\nAirport columns:")
print(airports.columns.tolist())


# ==========================================
# 4. PREPARE AIRLINE DATA
# ==========================================

# Keep the original IATA airline code
airlines = airlines.rename(
    columns={
        "IATA_CODE": "AIRLINE"
    }
)

# Keep both:
# AIRLINE      = airline code
# AIRLINE_NAME = full airline name

airlines = airlines[
    ["AIRLINE", "AIRLINE"]
].copy()

airlines = airlines.rename(
    columns={
        "AIRLINE": "AIRLINE_NAME"
    }
)