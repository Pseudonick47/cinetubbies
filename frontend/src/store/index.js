import Vue from 'vue';
import Vuex from 'vuex';

import {
  alert,
  auth,
  props,
  systemAdmin
} from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    alert,
    auth,
    props,
    systemAdmin
  }
};

export default new Vuex.Store(storeData);
