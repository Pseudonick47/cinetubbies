import * as _ from 'lodash';
import { PropReservation } from 'Models/prop-reservation.model';

const namespaced = true;

const state = {
  reservations: []
};

const getters = {
  all: (state) => state.reservations,
  one: (state) => (id) => state.reservations[id]
};

const mutations = {
  setReservations(state, reservations) {
    state.reservations = _.map(reservations, (r) => new PropReservation(r));
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
