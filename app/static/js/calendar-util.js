/**
 * days and times a tutor is available
 *
 * @typedef {Object} Availability
 * @property {Number} DayUTC
 * @property {string} TimeUTC - in "HH:MM" format
 */
// TODO: add function to account for Override availabilities

/**
 *
 * @param {Array.<Number>} defaultAvailableDays
 * @returns {Array.<Date>} unavailable dates for the next 30 days
 */
export const createDefaultRestrictedDates = (defaultAvailableDays) => {
  const restrictedDates = [];

  for (let i = 0; i <= 30; i++) {
    const nextDay = new Date();
    nextDay.setUTCDate(nextDay.getUTCDate() + i);
    const dayIsAvailable = defaultAvailableDays.includes(nextDay.getUTCDay());
    if (!dayIsAvailable) {
      restrictedDates.push(nextDay);
    }
  }

  return restrictedDates;
};

/**
 * use the default availability to create an object mapping a date string 'mm-dd'
 * to an array of Date objects representing time slots
 *
 * @param {Array.<Availability>} defaultAvailability
 */
export const createDefaultTimeSlots = (defaultAvailability) => {
  // key is MM-DD, value is array of Date objects
  const timeSlots = {};
  for (let i = 0; i <= 30; i++) {
    const nextDay = new Date();
    nextDay.setUTCDate(nextDay.getUTCDate() + i);

    const timeSlotKey = `${nextDay
      .getUTCMonth()
      .toString()
      .padStart(2, '0')}-${nextDay.getUTCDate().toString().padStart(2, '0')}`;
    timeSlots[timeSlotKey] = [];
    const availableTimes = defaultAvailability
      .filter((a) => a.DayUTC === nextDay.getUTCDay())
      .map((a) => {
        const [utcHours, utcMinutes] = a.TimeUTC.split(':').map((x) =>
          Number(x)
        );
        const timeSlot = new Date(nextDay);
        timeSlot.setUTCHours(utcHours, utcMinutes);
        return timeSlot;
      });
    availableTimes.forEach((timeSlot) => {
      console.log(timeSlot, typeof timeSlot);
      timeSlots[timeSlotKey].push(timeSlot);
    });
  }
  return timeSlots;
};
