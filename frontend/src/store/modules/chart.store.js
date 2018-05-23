const state = {
  labelsWeek: [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  ],
  labelsMonth: [
    '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '10',
    '11', '12', '13', '14', '15',
    '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25',
    '26', '27', '28', '29', '30',
    '31'
  ],
  labelsYear: [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ],
  labelsAll: [ 'Overall' ]
};

const getters = {
  labelsWeek: (state) => state.labelsWeek,
  labelsMonth: (state) => state.labelsMonth,
  labelsYear: (state) => state.labelsYear,
  labelsAll: (state) => state.labelsAll
};

export {
  state,
  getters
};