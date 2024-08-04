const TIME_OPTIONS = {
  locale: 'en-US',
  options: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  },
};

/**
 * takes the array of {'TimeSlot': "", 'BookingID': 0} and creates a map where the key is the formatted string
 * and the value is array of {'time': Date, 'id': 0}
 * @param {*} dbTimeSlots
 * @returns
 */
export const mapTimeSlotsFromDB = (dbTimeSlots) => {
  const timeSlots = {};
  for (const timeSlot of dbTimeSlots) {
    let thisDate = new Date(timeSlot['TimeSlot']);
    let timeSlotKey = formatDayKey(thisDate);
    if (timeSlots[timeSlotKey] === undefined) {
      timeSlots[timeSlotKey] = [];
    }
    timeSlots[timeSlotKey].push({ time: thisDate, id: timeSlot['BookingID'] });
  }
  return timeSlots;
};

/**
 * grabs the timeslots for selectedDate, day before, and day after and returns them in an object.
 *
 * @param {Date} selectedDate
 * @param {Object} timeSlots keys are localedatestrings and value is Array.<Date>
 */
export const getSelectedTimeSlots = (selectedDate, timeSlots) => {
  const previousDay = new Date(selectedDate);
  previousDay.setUTCDate(selectedDate.getUTCDate() - 1);
  const previousDayKey = formatDayKey(previousDay);

  const nextDay = new Date(selectedDate);
  nextDay.setUTCDate(selectedDate.getUTCDate() + 1);
  const nextDayKey = formatDayKey(nextDay);

  const previousTimeSlots = timeSlots[previousDayKey];
  const selectedTimeSlots = timeSlots[formatDayKey(selectedDate)];
  const nextTimeSlots = timeSlots[nextDayKey];

  return {
    previous: previousTimeSlots,
    selected: selectedTimeSlots,
    next: nextTimeSlots,
  };
};

/**
 * handler for selection of a date on the calendar.
 * renders elements for the timeslots based on which date is selected.
 *
 * @param {*} event
 */
export const updateTimeSlots = (event) => {
  const selectedDate = new Date(event.detail.value);
  renderDateHeaders(selectedDate);

  const timeSlots = window.timeSlots;
  const selectedTimeSlots = getSelectedTimeSlots(selectedDate, timeSlots);
  // access the templates to be cloned and other elements which hold the clones
  const timeslotTemplate = document.getElementById('timeslot-card');
  const timeSlotEmptyTemplate = document.getElementById('timeslot-empty-card');
  const previousDateElement = document.getElementById('timeslot-previous');
  const selectedDateElement = document.getElementById('timeslot-selected');
  const nextDateElement = document.getElementById('timeslot-next');

  // clear any timeslot child elements already present
  previousDateElement.innerHTML = '';
  selectedDateElement.innerHTML = '';
  nextDateElement.innerHTML = '';

  // clone the template and insert time values for the three relevant dates
  const numTimeSlots = 9;
  let numChild;
  let clone;
  let button;

  // previous
  selectedTimeSlots.previous?.forEach(({ time, id }) => {
    clone = timeslotTemplate.content.cloneNode(true);
    button = clone.querySelector('.time-slot__time');
    button.textContent = time.toLocaleTimeString(
      TIME_OPTIONS.locale,
      TIME_OPTIONS.options
    );
    button.dataset.id = id;
    button.onclick = selectTimeSlot;
    previousDateElement.appendChild(clone);
  });
  numChild = previousDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    previousDateElement.appendChild(clone);
  }

  // selected
  selectedTimeSlots.selected?.forEach(({ time, id }) => {
    clone = timeslotTemplate.content.cloneNode(true);
    button = clone.querySelector('.time-slot__time');
    button.textContent = time.toLocaleTimeString(
      TIME_OPTIONS.locale,
      TIME_OPTIONS.options
    );
    button.dataset.id = id;
    button.onclick = selectTimeSlot;
    selectedDateElement.appendChild(clone);
  });
  numChild = selectedDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    selectedDateElement.appendChild(clone);
  }

  // next
  selectedTimeSlots.next?.forEach(({ time, id }) => {
    clone = timeslotTemplate.content.cloneNode(true);
    button = clone.querySelector('.time-slot__time');
    button.textContent = time.toLocaleTimeString(
      TIME_OPTIONS.locale,
      TIME_OPTIONS.options
    );
    button.dataset.id = id;
    button.onclick = selectTimeSlot;
    nextDateElement.appendChild(clone);
  });
  numChild = nextDateElement.childElementCount;
  while (numChild++ < numTimeSlots) {
    clone = timeSlotEmptyTemplate.content.cloneNode(true);
    nextDateElement.appendChild(clone);
  }
};

const renderDateHeaders = (selectedDate) => {
  /*
   NOTE: instead of adding the day-type data attribute to the markup, you can
   reuse the getSelectedTimeSlots function
  */
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
};

/**
 * helper to consistently build key from a given Date which maps to the global timeSlots values
 *
 * @param {Date} date
 * @returns
 */
const formatDayKey = (date) => {
  const DATE_FORMAT = {
    locales: 'en-US',
    options: { month: '2-digit', day: '2-digit', year: 'numeric' },
  };
  return date.toLocaleDateString(DATE_FORMAT.locales, DATE_FORMAT.options);
};

const getAvailableDays = (dbTimeSlots) => {
  const uniqueDays = new Set();

  dbTimeSlots
    .map((x) => x['TimeSlot'])
    .forEach((date) => {
      const dayString = new Date(date).toDateString();
      uniqueDays.add(dayString);
    });

  return Array.from(uniqueDays).map((d) => new Date(d));
};

let PREV_SELECTED_BTN = null;
const selectTimeSlot = (event) => {
  const currBtn = event.target;
  if (PREV_SELECTED_BTN && PREV_SELECTED_BTN !== currBtn) {
    PREV_SELECTED_BTN.classList.remove('time-slot__time-toggled');
  }
  if (PREV_SELECTED_BTN !== currBtn) {
    currBtn.classList.toggle('time-slot__time-toggled');
  }
  PREV_SELECTED_BTN = currBtn;
  window.selectedBookingID = currBtn.dataset.id;
};

export const configureCalendar = (dbTimeSlots) => {
  // configure calendar
  const calendar = document.getElementById('calendar');
  calendar.min = new Date();
  const thirtyDaysAway = new Date();
  thirtyDaysAway.setDate(new Date().getDate() + 30);
  calendar.max = thirtyDaysAway;
  calendar.hideOtherMonthDays = true;
  calendar.importantDates = getAvailableDays(dbTimeSlots);
  calendar.addEventListener('change', updateTimeSlots);

  // // refresh calendar on initial load
  updateTimeSlots({ detail: { value: calendar.min.toISOString() } });
};
