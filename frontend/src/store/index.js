import Vue from 'vue';
import Vuex from 'vuex';

import { auth, alert } from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    auth,
    alert
  }
};

export default new Vuex.Store(storeData);
