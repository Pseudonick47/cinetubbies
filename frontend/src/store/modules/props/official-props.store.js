import { Prop } from 'Models/prop.model';

const namespaced = true;

const state = {
  props: [],
  count: 0
};

const getters = {
  all: (state) => state.props,
  one: (state) => (id) => _.find(state.props, 'id'),
  count: (state) => state.count
};

const mutations = {
  setProps(state, props) {
    state.props = _.map(props, p => new Prop(p));
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
