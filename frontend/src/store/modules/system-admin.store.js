const namespaced = true;

const state = {
  data: [],
  page: 1,
  entriesPerPage: 8,
  count: 0
};

const getters = {
  data: (state) => state.data,
  page: (state) => state.page,
  entriesPerPage: (state) => state.entriesPerPage,
  count: (state) => state.count
};

const mutations = {
  setData(state, data) {
    state.data = data;
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
  namespaced,
  state,
  getters,
  mutations
};
