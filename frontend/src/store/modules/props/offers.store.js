import * as _ from 'lodash';
import { PropOffer } from 'Models/prop-offer.model';

const namespaced = true;

const state = {
  offers: []
};

const getters = {
  all: (state) => state.offers,
  one: (state) => (id) => state.offers[id]
};

const mutations = {
  set(state, offers) {
    state.offers = _.map(offers, (o) => new PropOffer(o));
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
