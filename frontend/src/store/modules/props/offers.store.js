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
  },

  delete(state, id) {
    const index = _.findIndex(state.offers, (p) => p.id == id);
    state.offers.splice(index, 1);
  },

  insert(state, offer) {
    state.offers.push(new PropOffer(offer));
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
