-- SQLBook: Code

USE flight_pulse;

-- 1. Check total flights
SELECT COUNT(*) AS total_flights
FROM flights;

-- 2. Check average departure delay
SELECT ROUND(AVG(departure_delay), 2) AS avg_departure_delay
FROM flights;

-- 3. Count flights by airline
SELECT airline_code, COUNT(*) AS total_flights
FROM flights
GROUP BY airline_code
ORDER BY total_flights DESC;

-- 4. Count flights by delay status
SELECT delay_status, COUNT(*) AS flight_count
FROM flights
GROUP BY delay_status
ORDER BY flight_count DESC;

-- 5. Top 10 busiest routes
SELECT origin_airport, destination_airport,
       COUNT(*) AS total_flights
FROM flights
GROUP BY origin_airport, destination_airport
ORDER BY total_flights DESC
LIMIT 10;
