const state = {
  ticketsHeaders: [
    { text: 'Movie', sortable: false },
    { text: 'Auditorium', sortable: false },
    { text: 'Seat', sortable: false },
    { text: 'Date', sortable: false },
    { text: 'Time', sortable: false },
    { text: 'Original price(din)', sortable: false },
    { text: 'Discount(%)', sortable: false }
  ]
};

const getters = {
  ticketsHeaders: (state) => state.ticketsHeaders
};

export {
  state,
  getters
};
