import Vue from 'vue';
import Vuex from 'vuex';

import {
  alert,
  auth,
  categories,
  systemAdmin
} from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    alert,
    auth,
    categories,
    systemAdmin
  }
};

export default new Vuex.Store(storeData);
