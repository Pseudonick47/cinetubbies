import Vue from 'vue';
import Vuex from 'vuex';

import {
  alert,
  auth,
  props,
  reservations,
  systemAdmin,
  repertoire,
  ticketsOnSale,
  showtimes,
  movies,
  chart
} from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    alert,
    auth,
    props,
    reservations,
    systemAdmin,
    repertoire,
    ticketsOnSale,
    showtimes,
    movies,
    chart
  }
};

export default new Vuex.Store(storeData);
