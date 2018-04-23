
const state = {
  theaters: [],
  page: 1,
  entriesPerPage: 10,
  count: 0
};

const getters = {
  theaters: (state) => state.theaters,
  page: (state) => state.page,
  entriesPerPage: (state) => state.entriesPerPage,
  theatersCount: (state) => state.count
};

const mutations = {
  setTheaters(state, theaters) {
    state.theaters = theaters;
  },
  setEntriesPerPage(state, num) {
    state.num = num;
  },
  setPage(state, page) {
    state.page = page;
  },
  setCount(state, count) {
    state.count = count;
  }
};

export {
  state,
  getters,
  mutations
};
