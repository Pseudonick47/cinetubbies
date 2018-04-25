import * as _ from 'lodash';

const namespaced = true;

const state = {
  data: [],
  page: 1,
  entriesPerPage: 8,
  count: 0,
  theaterAdmins: []
};

const getters = {
  data: (state) => state.data,
  page: (state) => state.page,
  entriesPerPage: (state) => state.entriesPerPage,
  count: (state) => state.count,
  theaterAdmins: (state) => state.theaterAdmins,
  theaterAdmin: (state) => (id) => _.find(state.theaterAdmins, [ 'id', id ])
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
  },
  setTheaterAdmins(state, admins) {
    state.theaterAdmins = admins;
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
