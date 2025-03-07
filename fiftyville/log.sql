-- Keep a log of any SQL queries you execute as you solve the mystery.


-- STEP 1
--
-- Look at the report made on the day of the crime
SELECT description FROM crime_scene_reports
WHERE year = 2023
AND month = 7
AND day = 28;
-- Result:
-- Took place at 10.15AM at Humphrey Street bakery
-- 3 interviews recorded (all mentions bakery)


-- STEP 2
--
-- Read transcript(incl. names) of interviews regarding theft
SELECT name, transcript FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28;
-- Result:
-- Ruth: thief gets into car within 10 min of theft.
-- Eugene: Saw thief at ATM(Legget Street) withdrawing.
-- Raymond: Thief talked on phone >1min. Plans to take earliest flight next day. Ask other end of call to buy ticket.
-- (Lilly: Courthouse has rooster who crows at 6AM. Her sons, Robert and Patrick took the rooster. Sons are now in Paris.) - May be of interest.


--STEP 3
--
-- ID license plates that exited on the day of the theft at 10.15-25
SELECT name, license_plate FROM people
WHERE license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25);
-- Result:
-- Vanessa - 5P2BI95
-- Barry - 6P58WS2
-- Iman - L93JTIZ
-- Sofia - G412CB7
-- Luca - 4328GD8
-- Diana - 322W7JE
-- Kelsey - 0NTHK55
-- Bruce - 94KL13X


-- STEP 4
--
-- Check ATM transactions from the day and match through account number
SELECT name FROM people
WHERE id IN
(SELECT person_id FROM bank_accounts
WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND year = 2023
AND month = 7
AND day = 28));
-- Result:
-- Kenny
-- Iman
-- Benista
-- Taylor
-- Brooke
-- Luca
-- Diana
-- Bruce


-- SUSPECT COUNT:
-- License plate and ATM correlations:
-- Iman
-- Luca
-- Diana
-- Bruce


-- Step 5
--
-- Get names of caller and reciever from log of calls on that day that lasted < 60sec
SELECT p1.name as caller_name, p2.name as receiver_name
FROM phone_calls
JOIN people p1 ON phone_calls.caller = p1.phone_number
JOIN people p2 ON phone_calls.receiver = p2.phone_number
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;
-- Result:
-- Callers that are also suspects:
-- Bruce
-- Diana


-- STEP 6
--
-- Check for earliest flight on 29/7/23 and check destination airport/city
SELECT flights.*, airports.id, airports.full_name, airports.city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29
ORDER BY flights.hour ASC;
-- Result:
-- Dest. Airport with ID.4 = LaGuardia Airport, New York City


-- STEP 7
--
-- Get name of passengers who took the early flight on 29/7/23 to CDG, Paris, France
SELECT name FROM people
WHERE passport_number IN
(SELECT passport_number FROM passengers
WHERE flight_id In
(SELECT id FROM flights
WHERE destination_airport_id IN
(SELECT id FROM airports
WHERE city = 'New York City'
AND year = 2023
AND month = 7
AND day = 29 )));
-- Result:
-- Passenger who are also suspects:
-- Bruce


-- STEP 8
--
-- Find accomplice by checking who Bruce was calling on 28/7/23
SELECT p1.name as caller_name, p2.name as receiver_name
FROM phone_calls
JOIN people p1 ON phone_calls.caller = p1.phone_number
JOIN people p2 ON phone_calls.receiver = p2.phone_number
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller_name = 'Bruce';
-- Result:
-- Bruce called Robin on 28/7/23 for less than 1min.
-- From this we can deduce that Robin must have been the accomplice.
