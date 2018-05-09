const state = {
  showtimeHeaders: [
    { text: 'Show', sortable: false },
    { text: 'Auditorium', sortable: false },
    { text: 'Date', sortable: false },
    { text: 'Time', sortable: false },
    { text: 'Price($)', sortable: false }
  ]
};

const getters = {
  showtimeHeaders: (state) => state.showtimeHeaders
};

export {
  state,
  getters
};
