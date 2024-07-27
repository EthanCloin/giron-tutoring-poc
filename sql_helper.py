"""handy builder so i don't have to type out a bunch of numbers to build the dummy data"""


def main():
    pass


def build_tutoravailability_testdata():
    # structure: "(TutorAvailabilityID, TutorID, DayUTC, TimeUTC)"
    tutor_availability_id = 1
    for tutor_id in range(1, 4):
        for day in range(1, 6):
            for hour in range(13, 22):
                availability_record = (
                    f'({tutor_availability_id}, {tutor_id}, {day}, "{hour}:00"),'
                )
                print(availability_record)
                tutor_availability_id += 1


# def create_default_time_slots(default_availability: list) -> dict[str, list[datetime]]:
#     time_slots = {}
#     LOCALE_DATE_FORMAT = "%m-%d"

#     for i in range(31):
#         next_day = datetime.now(timezone.utc) + timedelta(days=i)
#         time_slot_key = next_day.strftime(LOCALE_DATE_FORMAT)
#         time_slots[time_slot_key] = []

#         available_times = [
#             datetime(
#                 year=next_day.year,
#                 month=next_day.month,
#                 day=next_day.day,
#                 hour=int(time.split(":")[0]),
#                 minute=int(time.split(":")[1]),
#             )
#             for avail in default_availability
#             if avail.get("DayUTC") == next_day.weekday()
#             for time in [avail.get("TimeUTC")]
#         ]

#         time_slots[time_slot_key].extend(available_times)

#     return time_slots


if __name__ == "__main__":
    pass
