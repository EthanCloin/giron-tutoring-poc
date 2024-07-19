/**
 * days and times a tutor is available
 *
 * @typedef {Object} Availability
 * @property {Number} DayUTC
 * @property {string} TimeUTC - in "HH:MM" format
 */

/**
 *
 * @param {Array.<Number>} defaultAvailableDays
 * @returns {Array.<Date>} unavailable dates for the next 30 days
 */
export const determineRestrictedDates = (defaultAvailability) => {
  const restrictedDates = [];

  for (let i = 0; i <= 30; i++) {
    const nextDay = new Date();
    nextDay.setUTCDate(nextDay.getUTCDate() + i);
    const dayIsAvailable = defaultAvailability.includes(nextDay.getUTCDay());
    if (!dayIsAvailable) {
      restrictedDates.push(nextDay);
    }
  }

  return restrictedDates;
};
