const state = {
  showtimeHeaders: [
    { text: 'Movie', sortable: false },
    { text: 'Auditorium', sortable: false },
    { text: 'Date', sortable: false },
    { text: 'Time', sortable: false },
    { text: 'Price(din)', sortable: false }
  ]
};

const getters = {
  showtimeHeaders: (state) => state.showtimeHeaders
};

export {
  state,
  getters
};
