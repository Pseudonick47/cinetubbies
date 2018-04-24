import Vue from 'vue';
import Vuex from 'vuex';

import { auth, alert, theaters } from './modules';

Vue.use(Vuex);

const storeData = {
  modules: {
    auth,
    alert,
    theaters
  }
};

export default new Vuex.Store(storeData);
