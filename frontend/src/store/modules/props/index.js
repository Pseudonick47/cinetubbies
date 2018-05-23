import * as categories from './categories.store';
import * as offers from './offers.store';
import * as reservations from './reservations.store';

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
  },

  insertProp(state, prop) {
    state.props.push(new Prop(prop));
    state.props = _.sortBy(state.props, (p) => _.lowerCase(p.title));
  },

  updateProp(state, prop) {
    const p = _.find(state.props, [ 'id', prop.id ]);
    if (p) {
      p.update(prop);
    }
  },

  deleteProp(state, id) {
    console.log(state.props);
    _.remove(state.props, (p) => p.id == id);
    console.log(state.props);
  }
};

const modules = {
  categories,
  offers,
  reservations
};

export {
  namespaced,
  state,
  getters,
  mutations,
  modules
};
