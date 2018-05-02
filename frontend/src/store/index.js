import Vue from 'vue';
import Vuex from 'vuex';

import {
  alert,
  auth,
  props,
  reservations,
  systemAdmin
} from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    alert,
    auth,
    props,
    reservations,
    systemAdmin
  }
};

export default new Vuex.Store(storeData);
