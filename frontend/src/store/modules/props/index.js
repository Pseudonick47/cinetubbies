import * as categories from './categories.store';
import * as official from './official-props.store';
import * as reservations from './reservations.store';
import * as used from './used-props.store';

import { Prop } from 'Models/prop.model';

const namespaced = true;

const state = {
  props: [],
  prop: null,
  count: 0
};

const getters = {
  all: (state) => state.props,
  one: (state) => (id) => {
    if (this.prop && this.prop.id === id) {
      return this.prop;
    }
    return _.find(state.props, [ 'id', id ]);
  },
  count: (state) => state.count,
  get: (state) => state.prop
};

const mutations = {
  setProps(state, props) {
    state.props = _.map(props, p => new Prop(p));
  },

  setProp(state, prop) {
    state.prop = new Prop(prop);
  },

  setCount(state, count) {
    state.count = count;
  }
};

const modules = {
  categories,
  official,
  reservations,
  used
};

export {
  namespaced,
  state,
  getters,
  mutations,
  modules
};
