INSERT INTO Tutors (TutorID, Name, Email, Phone)
VALUES (
        1,
        'Ethan Cloin',
        'ethan@email.com',
        '123-123-1234'
    ) ON CONFLICT (TutorID) DO NOTHING;
INSERT INTO TutorAvailability (AvailabilityID, TutorID, DayUTC, TimeUTC) --
-- set default availability 9-5 EST (13-21 UTC) weekdays
VALUES (1, 1, 1, "13:00"),
    (2, 1, 1, "14:00"),
    (3, 1, 1, "15:00"),
    (4, 1, 1, "16:00"),
    (5, 1, 1, "17:00"),
    (6, 1, 1, "18:00"),
    (7, 1, 1, "19:00"),
    (8, 1, 1, "20:00"),
    (9, 1, 1, "21:00") ON CONFLICT (AvailabilityID) DO NOTHING;