import Vue from 'vue';
import Vuex from 'vuex';

import {
  alert,
  auditoriums,
  auth,
  chart,
  miscellaneous,
  movies,
  props,
  repertoire,
  reservations,
  showtimes,
  systemAdmin,
  ticketsOnSale
} from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    alert,
    auditoriums,
    auth,
    chart,
    miscellaneous,
    movies,
    props,
    repertoire,
    reservations,
    showtimes,
    systemAdmin,
    ticketsOnSale
  }
};

export default new Vuex.Store(storeData);
