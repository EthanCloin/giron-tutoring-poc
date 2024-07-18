-- build all the tables, dropping first to start fresh
DROP TABLE IF EXISTS Tutors;
CREATE TABLE Tutors (
    TutorID INTEGER PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    Phone TEXT
);
DROP TABLE IF EXISTS Clients;
CREATE TABLE Clients (
    ClientID INTEGER PRIMARY KEY,
    Name TEXT,
    Email TEXT,
    Phone TEXT
);
DROP TABLE IF EXISTS TutorAvailability;
CREATE TABLE TutorAvailability (
    AvailabilityID INTEGER PRIMARY KEY,
    TutorID INTEGER,
    -- maybe add constraint to keep the int value between 0-6
    DayUTC INTEGER NOT NULL,
    -- HH:MM
    TimeUTC TEXT NOT NULL,
    OverrideDatetimeUTC DATETIME DEFAULT NULL,
    FOREIGN KEY(TutorID) REFERENCES Tutors(TutorID)
);
DROP TABLE IF EXISTS Bookings;
CREATE TABLE Bookings (
    BookingID INTEGER PRIMARY KEY,
    AvailabilityID INTEGER,
    ClientID INTEGER,
    TutorID INTEGER,
    -- unclear if cascade is appropriate here
    FOREIGN KEY(AvailabilityID) REFERENCES Products(AvailabilityID),
    -- ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY(TutorID) REFERENCES Tutors(TutorID)
);