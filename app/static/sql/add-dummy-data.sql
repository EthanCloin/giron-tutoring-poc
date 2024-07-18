INSERT INTO Tutors (TutorID, Name, Email, Phone)
VALUES (
        1,
        'Ethan Cloin',
        'ethan@email.com',
        '123-123-1234'
    ) ON CONFLICT (TutorID) DO NOTHING -- set default availability 9-5 EST weekdays
    -- INSERT INTO Availability (AvailabilityID, TutorID, DayUTC, TimeUTC)
    -- VALUES (1, 1, 1,)