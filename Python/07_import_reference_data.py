
import pandas as pd
import mysql.connector
from getpass import getpass
from mysql.connector import Error

# ==========================================
# FLIGHT PULSE - IMPORT REFERENCE DATA
# ==========================================

print("\n========================================")
print(" FLIGHT PULSE - DATA IMPORT")
print("========================================")

connection = None
cursor = None

try:
    # --------------------------------------
    # 1. CONNECT TO MYSQL
    # --------------------------------------

    print("\nEnter your MySQL credentials.")

    mysql_user = input("MySQL username [root]: ").strip() or "root"
    mysql_password = getpass("MySQL password: ")

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user=mysql_user,
        password=mysql_password,
        database="flight_pulse",
        connection_timeout=10
    )

    cursor = connection.cursor()

    print("\nConnected to flight_pulse successfully!")

    # --------------------------------------
    # 2. IMPORT AIRLINES
    # --------------------------------------

    print("\nLoading airlines.csv...")

    airlines = pd.read_csv(
        r"D:\Flight_Pulse\Data\airlines.csv"
    )

    airlines.columns = airlines.columns.str.strip()

    required_airline_columns = ["IATA_CODE", "AIRLINE"]

    if not all(
        column in airlines.columns
        for column in required_airline_columns
    ):
        raise ValueError(
            "Unexpected airline CSV columns: "
            + str(airlines.columns.tolist())
        )

    airlines = airlines.rename(columns={
        "IATA_CODE": "airline_code",
        "AIRLINE": "airline_name"
    })

    airlines = airlines.dropna(
        subset=["airline_code"]
    )

    airline_data = []

    for row in airlines[
        ["airline_code", "airline_name"]
    ].itertuples(index=False, name=None):

        code = str(row[0]).strip()
        name = None if pd.isna(row[1]) else str(row[1]).strip()

        airline_data.append((code, name))

    airline_sql = """
        INSERT INTO airlines (airline_code, airline_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            airline_name = VALUES(airline_name)
    """

    cursor.executemany(airline_sql, airline_data)
    connection.commit()

    print("Airline records processed:", len(airline_data))

    # --------------------------------------
    # 3. IMPORT AIRPORTS
    # --------------------------------------

    print("\nLoading airports.csv...")

    airports = pd.read_csv(
        r"D:\Flight_Pulse\Data\airports.csv",
        low_memory=False
    )

    airports.columns = airports.columns.str.strip()

    airport_mapping = {
        "IATA_CODE": "airport_code",
        "AIRPORT": "airport_name",
        "CITY": "city",
        "STATE": "state",
        "COUNTRY": "country",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude"
    }

    missing_columns = [
        column for column in airport_mapping
        if column not in airports.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing airport CSV columns: "
            + str(missing_columns)
        )

    airports = airports.rename(columns=airport_mapping)

    airport_columns = [
        "airport_code",
        "airport_name",
        "city",
        "state",
        "country",
        "latitude",
        "longitude"
    ]

    airports = airports[airport_columns].dropna(
        subset=["airport_code"]
    )

    def convert_value(value):
        if pd.isna(value):
            return None

        if hasattr(value, "item"):
            value = value.item()

        return value

    airport_data = []

    for row in airports.itertuples(index=False, name=None):
        values = [convert_value(value) for value in row]

        # Ensure airport codes are strings
        values[0] = str(values[0]).strip()

        airport_data.append(tuple(values))

    airport_sql = """
        INSERT INTO airports (
            airport_code, airport_name, city,
            state, country, latitude, longitude
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            airport_name = VALUES(airport_name),
            city = VALUES(city),
            state = VALUES(state),
            country = VALUES(country),
            latitude = VALUES(latitude),
            longitude = VALUES(longitude)
    """

    cursor.executemany(airport_sql, airport_data)
    connection.commit()

    print("Airport records processed:", len(airport_data))

    # --------------------------------------
    # 4. VERIFY IMPORT
    # --------------------------------------

    cursor.execute("SELECT COUNT(*) FROM airlines")
    airline_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM airports")
    airport_count = cursor.fetchone()[0]

    print("\n========================================")
    print(" IMPORT RESULTS")
    print("========================================")

    print("Airlines in MySQL:", airline_count)
    print("Airports in MySQL:", airport_count)

    cursor.execute("""
        SELECT airline_code, airline_name
        FROM airlines
        LIMIT 5
    """)

    print("\nSample airlines:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
        SELECT airport_code, city, country
        FROM airports
        LIMIT 5
    """)

    print("\nSample airports:")
    for row in cursor.fetchall():
        print(row)

    print("\nREFERENCE DATA IMPORT COMPLETE")

except Error as error:
    if connection is not None and connection.is_connected():
        connection.rollback()

    print("\nMYSQL ERROR:")
    print(error)

    print(
        "\nIf access is denied, verify the username and password "
        "used by your MySQL server."
    )

except (OSError, ValueError, KeyError) as error:
    if connection is not None and connection.is_connected():
        connection.rollback()

    print("\nDATA OR FILE ERROR:")
    print(error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()

    print("\nMySQL connection closed.")
