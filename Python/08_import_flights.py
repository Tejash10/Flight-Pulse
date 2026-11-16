-- Active: 1790838994905@@localhost@3306@mysql

import pandas as pd
import mysql.connector
from getpass import getpass

csv_path = r"D:\Flight_Pulse\Data\flights_sql.csv"

username = input("MySQL username: ")
password = getpass("MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user=loalhost,
        password=tjash23
        database="flight_pulse"
    )

    print("MySQL connected successfully!")

    df = pd.read_csv(csv_path, nrows=1000)
    print("Rows ready to import:", len(df))
    print("Columns:", list(df.columns))

    connection.close()

except mysql.connector.Error as error:
    print("MySQL connection failed:", error)
except FileNotFoundError:
    print("CSV file not found. Check the file path.")
