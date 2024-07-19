"""handy builder so i don't have to type out a bunch of numbers to build the dummy data"""

tutor_availability_id = 1
for tutor_id in range(1, 4):
    for day in range(1, 6):
        for hour in range(13, 22):
            availability_record = (
                f'({tutor_availability_id}, {tutor_id}, {day}, "{hour}:00"),'
            )
            print(availability_record)
            tutor_availability_id += 1
