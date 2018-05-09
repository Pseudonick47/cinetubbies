const state = {
  headers: [
    { text: 'Show', sortable: false, value: 'movie' },
    { text: 'Auditorium', sortable: false },
    { text: 'Date', sortable: false },
    { text: 'Time', sortable: false },
    { text: 'Price($)', sortable: false }
  ]
};

const getters = {
  headers: (state) => state.headers
};

export {
  state,
  getters
};
