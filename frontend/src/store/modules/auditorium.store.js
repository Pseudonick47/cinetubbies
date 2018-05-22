import * as _ from 'lodash';
import { Reward } from 'Models/reward.model';
import TheatersController from 'Controllers/theaters.controller';
import TheatersApi from 'Api/theaters.service';

const state = {
  auditoriums: {}
};

const getters = {
  auditoriums: (state) => state.auditoriums,
  auditorium: (state) => (id) => state.auditoriums[id]
};

const actions = {
  async fetchAuditoriums({ commit }, theaterId) {
    let auditoriums = await TheatersApi.getAuditoriums(theaterId);
    auditoriums = TheatersController.mapAuditoriums(auditoriums.data);
    commit('setAuditoriums', auditoriums);
  },
}

const mutations = {
  setAuditoriums(state, data) {
    _.forEach(data, x => state.auditoriums[x.id] = x);
  }
};

export {
  actions,
  state,
  getters,
  mutations
};
