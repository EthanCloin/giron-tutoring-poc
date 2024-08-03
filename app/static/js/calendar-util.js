/**
 * days and times a tutor is available
 *
 * @typedef {Object} Availability
 * @property {Number} DayUTC
 * @property {string} TimeUTC - in "HH:MM" format
 */

// TODO: add function to account for Override availabilities

const LOCALE_DATE_OPTIONS = {
  locales: 'en-US',
  options: { month: '2-digit', day: '2-digit' },
};

export const TIME_OPTIONS = {
  locale: 'en-US',
  options: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  },
};
/**
 *
 * @param {Array.<Number>} defaultAvailableDays
 * @returns {Array.<Date>} unavailable dates for the next 30 days
 */
export const createDefaultRestrictedDates = (defaultAvailableDays) => {
  // TODO: determine how this is offsetting availability from database by a day
  //  expecting tutorid=1 to have 9-5 M-F EST but it's S-Th now
  // OR maybe it's just looking wrong bc i'm allowing selection of days in the past
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
  // key is DateString, value is array of Date objects
  const timeSlots = {};

  for (let i = 0; i <= 30; i++) {
    const nextDay = new Date();
    nextDay.setUTCDate(nextDay.getUTCDate() + i);

    const timeSlotKey = nextDay.toLocaleDateString(LOCALE_DATE_OPTIONS);
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
      timeSlots[timeSlotKey].push(timeSlot);
    });
  }
  return timeSlots;
};

export const mapTimeSlotsFromDB = (dbTimeSlots) => {
  // TODO: make this work with the timeslots UI
  const timeSlots = {};
  for (const timeSlot of dbTimeSlots) {
    let thisDate = new Date(timeSlot);
    let timeSlotKey = thisDate.toLocaleDateString(
      LOCALE_DATE_OPTIONS.locales,
      LOCALE_DATE_OPTIONS.options
    );
    if (timeSlots[timeSlotKey] === undefined) {
      timeSlots[timeSlotKey] = [];
    }
    timeSlots[timeSlotKey].push(thisDate);
  }
  console.log(timeSlots);
  return timeSlots;
};

/**
 *
 * @param {Date} selectedDate
 * @param {*} timeSlots object whose keys are localedatestrings and value is Array.<Date>
 */
export const getSelectedTimeSlots = (selectedDate, timeSlots) => {
  const previousDay = new Date(selectedDate);
  previousDay.setUTCDate(selectedDate.getUTCDate() - 1);
  const previousDayKey = previousDay.toLocaleDateString(LOCALE_DATE_OPTIONS);

  const nextDay = new Date(selectedDate);
  nextDay.setUTCDate(selectedDate.getUTCDate() + 1);
  const nextDayKey = nextDay.toLocaleDateString(LOCALE_DATE_OPTIONS);

  const previousTimeSlots = timeSlots[previousDayKey];
  const selectedTimeSlots =
    timeSlots[selectedDate.toLocaleDateString(LOCALE_DATE_OPTIONS)];
  const nextTimeSlots = timeSlots[nextDayKey];

  return {
    previous: previousTimeSlots,
    selected: selectedTimeSlots,
    next: nextTimeSlots,
  };
};

export const updateTimeSlots = (event) => {
  const selectedDate = new Date(event.detail.value);
  const timeSlots = window.timeSlots;
  const selectedTimeSlots = getSelectedTimeSlots(selectedDate, timeSlots);
  // access the templates to be cloned and other elements which hold the clones
  const timeslotTemplate = document.getElementById('timeslot-card');
  const timeSlotEmptyTemplate = document.getElementById('timeslot-empty-card');
  const previousDateElement = document.getElementById('timeslot-previous');
  const selectedDateElement = document.getElementById('timeslot-selected');
  const nextDateElement = document.getElementById('timeslot-next');

  // Add date headers
  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });
  };
  const dateHeaderElements = document.querySelectorAll('.time-slot__date');
  dateHeaderElements.forEach((element) => {
    const dayType = element.getAttribute('data-day-type');
    if (dayType === 'previous') {
      element.textContent = formatDate(
        new Date(selectedDate.getTime() - 24 * 60 * 60 * 1000)
      );
    } else if (dayType === 'selected') {
      element.textContent = formatDate(selectedDate);
    } else {
      element.textContent = formatDate(
        new Date(selectedDate.getTime() + 24 * 60 * 60 * 1000)
      );
    }
  });

  // clear any timeslot child elements already present
  previousDateElement.innerHTML = '';
  selectedDateElement.innerHTML = '';
  nextDateElement.innerHTML = '';

  // clone the template and insert time values for the three relevant dates
  const numTimeSlots = 9;
  let numChild;
  let clone;
  let innerP;

  // previous
  selectedTimeSlots.previous?.forEach((time) => {
    clone = timeslotTemplate.content.cloneNode(true);
    innerP = clone.querySelector('.time-slot__time');
    innerP.textContent =
      time.toLocaleTimeString(TIME_OPTIONS.locale, TIME_OPTIONS.options) +
      'prev';
    previousDateElement.appendChild(clone);
  });
  numChild = previousDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    previousDateElement.appendChild(clone);
  }

  // selected
  selectedTimeSlots.selected?.forEach((time) => {
    clone = timeslotTemplate.content.cloneNode(true);
    innerP = clone.querySelector('.time-slot__time');
    innerP.textContent =
      time.toLocaleTimeString(TIME_OPTIONS.locale, TIME_OPTIONS.options) +
      'selected';
    selectedDateElement.appendChild(clone);
  });
  numChild = selectedDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    selectedDateElement.appendChild(clone);
  }

  // next
  selectedTimeSlots.next?.forEach((time) => {
    clone = timeslotTemplate.content.cloneNode(true);
    innerP = clone.querySelector('.time-slot__time');
    innerP.textContent =
      time.toLocaleTimeString(TIME_OPTIONS.locale, TIME_OPTIONS.options) +
      'next';
    nextDateElement.appendChild(clone);
  });
  numChild = nextDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    nextDateElement.appendChild(clone);
  }
};
