const namespaced = true;

const state = {
  drawer: null
};

const getters = {
  drawer: (state) => state.drawer,
  hasDrawer: (state) => state.drawer !== null
};

const mutations = {
  setDrawer(state, visible) {
    state.drawer = visible;
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
