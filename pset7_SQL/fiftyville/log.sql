-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Pset7 Fiftyville
-- https://cs50.harvard.edu/x/2021/psets/7/fiftyville/

-- get information about theft July 28, 2020.
SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street = 'Chamberlin Street';

-- Theft took place at 10:15 am courthouse.
-- Interviews were conducted with three witnesses and the courthouse is mentioned in each of their interview transcripts.

-- What does the witnesses says?
SELECT name, transcript FROM interviews WHERE year = 2020 AND month = 7 AND day = 28;

-- 1. The thief get into a car in the courthouse parking lot and drive away. VIEW SECURITY FOOTAGE from the courthouse parking lot, estimated time 10:25!
    -- NO DATA FROM SECURITY FOOTAGE.

-- 2. Earlier this morning, the thief there withdrawing some money by an ATM on Fifer Street.
    -- View ATM transactions:
    SELECT account_number, transaction_type, amount FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = 'Fifer Street';

    -- Find the first suspects, those who used the ATM on Fifer Street:
    SELECT name, phone_number, passport_number, license_plate FROM people
    INNER JOIN (SELECT person_id FROM bank_accounts INNER JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
        WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw')
    ON id = person_id;
    -- SUSPECTS:
        -- name	        phone_number	passport_number	license_plate
        -- Ernest	    (367) 555-5533	5773159633	    94KL13X
        -- Russell	    (770) 555-1861	3592750733	    322W7JE
        -- Roy	        (122) 555-4581	4408372428	    QX4YZN3
        -- Bobby	    (826) 555-1652	9878712108	    30G67EN
        -- Elizabeth	(829) 555-5269	7049073643	    L93JTIZ
        -- Danielle	    (389) 555-5198	8496433585	    4328GD8
        -- Madison	    (286) 555-6063	1988161715	    1106N58
        -- Victoria	    (338) 555-6650	9586786673	    8X428L0

-- 3. As the thief was leaving the courthouse, he called someone who talked to them for less than a minute.
--    In the call, the thief say that he were planning to take the earliest flight out of Fiftyville tomorrow.
--    The thief then asked the person on the other end of the phone to purchase the flight ticket.

    -- Сheck which of the suspects left the courthouse from 10:15 to 10:25. on July 28, 2020:
    SELECT suspects.name, courthouse_security_logs.license_plate FROM courthouse_security_logs
    INNER JOIN (SELECT people.name, people.license_plate FROM people
        INNER JOIN (SELECT person_id FROM bank_accounts INNER JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
            WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw')
        ON id = person_id) as suspects
    ON courthouse_security_logs.license_plate = suspects.license_plate WHERE hour = 10 AND minute >= 15 AND minute <= 25;
        -- The circle of suspects is narrowing:
            -- name	        phone_number	passport_number	license_plate
            -- Ernest	    (367) 555-5533	5773159633	    94KL13X
            -- Russell	    (770) 555-1861	3592750733	    322W7JE
            -- Elizabeth	(829) 555-5269	7049073643	    L93JTIZ
            -- Danielle	    (389) 555-5198	8496433585	    4328GD8

    -- Find suspects who, on July 28, 2020, withdrew money from an ATM on Fifer Street, left the courthouse from 10:15 to 10:25 and made a call in less than 1 minute:
    SELECT suspects_shortlist.name, suspects_shortlist.phone_number, suspects_shortlist.passport_number FROM phone_calls
    INNER JOIN (SELECT suspects.name, suspects.phone_number, suspects.passport_number FROM courthouse_security_logs
        INNER JOIN (SELECT people.name, people.phone_number, people.passport_number, people.license_plate FROM people
            INNER JOIN (SELECT person_id FROM bank_accounts INNER JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
                WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = 'Fifer Street' AND transaction_type = 'withdraw')
            ON id = person_id) as suspects
        ON courthouse_security_logs.license_plate = suspects.license_plate WHERE hour = 10 AND minute >= 15 AND minute <= 25) as suspects_shortlist
    ON suspects_shortlist.phone_number = phone_calls.caller WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;
    -- List of suspects:
        -- name	    phone_number        passport_number
        -- Ernest	(367) 555-5533      5773159633
        -- Russell	(770) 555-1861      3592750733

    -- Find the earliest flight from Fiftyville:
        --1. find all flights from Fiftyville on july 29, 2020;
        --2. replace id of the airports with their full names and find the earliest flight;
        SELECT flights_fiftyville.id, origin_airport.city as origin_city, destination_airport.city as destination_city, min(hour) as hour, minute
        FROM (SELECT * FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2020 AND month = 7 AND day = 29) as flights_fiftyville
        INNER JOIN airports as origin_airport ON origin_airport_id = origin_airport.id
        INNER JOIN airports as destination_airport ON destination_airport_id = destination_airport.id;
        -- id	origin_airport      destination_airport     hour   	minute
        -- 36	Fiftyville          London                  8	    20

        -- If the thief was on this flight, he fled to London!

    -- Find passengers on this flight:
        -- 1. define the flight id;
        -- 2. find passengers by flight id;
        SELECT passport_number, seat FROM passengers WHERE flight_id =
            (SELECT id FROM (SELECT * FROM flights WHERE origin_airport_id =
                (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2020 AND month = 7 AND day = 29)
            WHERE hour = (SELECT min(hour) FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2020 AND month = 7 AND day = 29));
        -- Passengers on the earliest flight from Fiftyville:
            -- passport_number	seat
            -- 7214083635	    2A
            -- 1695452385	    3B
            -- 5773159633	    4A
            -- 1540955065	    5C
            -- 8294398571	    6C
            -- 1988161715	    6D
            -- 9878712108	    7A
            -- 8496433585	    7B

    -- Compare the list of passengers with the list of suspects:
        -- 1. receive the passport numbers of passengers departing with the earliest flight from fiftyville on July 28, 2020;
        -- 2. exclude the "extra" passenger passport numbers and leave only the suspect passport numbers if they are on this list;
        -- 3. display the names of the suspects who were on the flight;
        SELECT name FROM people WHERE passport_number =
            (SELECT passport_number FROM passengers WHERE flight_id =
                (SELECT id FROM (SELECT * FROM flights WHERE origin_airport_id =
                    (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2020 AND month = 7 AND day = 29)
                WHERE hour = (SELECT min(hour) FROM flights WHERE origin_airport_id =
                    (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2020 AND month = 7 AND day = 29))
                    AND (passport_number = '5773159633' OR passport_number = '3592750733'))
    -- name: Ernest

    -- THE THIEF is ERNEST!!!
    -- THE THIEF ESCAPED TO: LONDON!!!

    -- Find the person the thief called after leaving the courthouse:
        -- 1. find the thief's phone number(assuming there is only one person in the database named Ernest);
        -- 2. find a call made from this number near the courthouse;
        -- 3. calculate the accomplice by phone number;
        SELECT name, phone_number, passport_number, license_plate FROM people WHERE phone_number =
            (SELECT receiver FROM phone_calls WHERE caller =
                (SELECT phone_number FROM people WHERE name = 'Ernest') AND year = 2020 AND month = 7 AND day = 28 AND duration < 60);
        -- name     | phone_number      | passport_number   | license_plate
        -- Berthold | (375) 555-8161    | -                 | 4V16VO0

        -- THIEF'S ACCOMPLICE is BERTHOLD!!!

