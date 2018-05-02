import * as _ from 'lodash';
import { User } from 'Models/user.model';

const state = {
  activeUser: null
};

const getters = {
  activeUser: (state) => state.activeUser,
  isLogged: (state) => !_.isEmpty(state.activeUser),
  isAnyAdmin: (state, getters) => getters.isLogged && state.activeUser.isAnyAdmin(),
  isAdmin: (state, getters) => getters.isLogged && state.activeUser.isAdmin(),
  isCinemaAdmin: (state, getters) => getters.isLogged && state.activeUser.isCinemaAdmin(),
  isFanZoneAdmin: (state, getters) => getters.isLogged && state.activeUser.isFanZoneAdmin(),
  activeUserRole: (state) => state.activeUser ? state.activeUser.role : 'guest'

};

const mutations = {
  deauth(state) {
    localStorage.clear();
    state.activeUser = null;
  },
  auth(state, activeUser) {
    const user = new User(activeUser);
    state.activeUser = user;
  },
  updateActiveUser(state, data) {
    state.activeUser.updateUser(data);
  },
  setAdminsTheater(state, theater) {
    state.activeUser.theater = theater;
  }
};

export {
  state,
  getters,
  mutations
};
