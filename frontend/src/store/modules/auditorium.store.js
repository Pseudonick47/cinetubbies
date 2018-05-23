import * as _ from 'lodash';
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
  fetchAuditoriums({ commit }, theaterId) {
    TheatersApi.getAuditoriums(theaterId).then((response) => {
      let auditoriums = TheatersController.mapAuditoriums(response.data);
      commit('setAuditoriums', auditoriums);
    });
  }
};

const mutations = {
  setAuditoriums(state, data) {
    _.forEach(data, x => {
      state.auditoriums[x.id] = x;
    });
  }
};

export {
  actions,
  state,
  getters,
  mutations
};
