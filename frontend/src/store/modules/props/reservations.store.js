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
  },

  delete(state, id) {
    const index = _.findIndex(state.reservations, (r) => r.id == id);
    state.reservations.splice(index, 1);
  },

  insert(state, reservation) {
    state.reservations.push(new PropReservation(reservation));
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
