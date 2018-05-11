import * as categories from './categories.store';
import * as official from './official-props.store';
import * as used from './used-props.store';

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

const modules = {
  categories,
  official,
  used
};

export {
  namespaced,
  state,
  getters,
  mutations,
  modules
};
