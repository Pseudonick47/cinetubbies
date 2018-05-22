const state = {
  showtimes: {},
  showtimeHeaders: [
    { text: 'Show', sortable: false },
    { text: 'Auditorium', sortable: false },
    { text: 'Date', sortable: false },
    { text: 'Time', sortable: false },
    { text: 'Price($)', sortable: false }
  ]
};

const getters = {
  showtimeHeaders: (state) => state.showtimeHeaders,
  showtimes: (state) => state.showtimes,
  showtime: (state) => (id) => state.showtimes[id],
  showtimeSeats: (state) => (id) => {
    return _.map(state.showtimes[id].seats, (x) => {
      return !x.taken;
    });
  }
};

const mutations = {
  setShowtimes(state, data) {
    _.forEach(data, x => state.showtimes[x.id] = x);
  },
  bookTicket(state, data) {
    _.forEach(data.seats, x => {
      state.showtimes[data.showtimeId].seats[x - 1].taken = 1;
    });
  },
  addShowtime(state, data) {
    state.showtimes[data.id] = data;
  }
};

export {
  state,
  getters,
  mutations
};
