import Vue from 'vue';
import Vuex from 'vuex';

import { auth, alert, systemAdmin } from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    auth,
    alert,
    systemAdmin
  }
};

export default new Vuex.Store(storeData);
