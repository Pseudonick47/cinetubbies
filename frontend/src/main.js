import Vue from 'vue';
import App from './App';
import router from './router';
import store from './store';
import Vuetify from 'vuetify';
import Axios from 'axios';
import 'vuetify/dist/vuetify.min.css';
import Config from './config';
import AlertHelper from './helpers/alert-helper';
import VeeValidate from 'vee-validate';
import * as VueGoogleMaps from 'vue2-google-maps';

import AuthController from 'Controllers/auth.controller';

Vue.config.productionTip = false;

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyDGSW_ia8ylzlAdER3ckEQW8UJ6MgTEnlQ',
    libraries: 'places',
    language: 'en'
  }
});

Vue.use(VeeValidate);
Vue.use(Vuetify);
Vue.prototype.router = router;
Vue.prototype.$alert = AlertHelper;

Axios.defaults.baseURL = Config.getApiUrl();
Axios.defaults.headers.Accept = 'application/json';
Axios.defaults.headers['Access-Control-Allow-Origin'] = '*';

AuthController.initStoreAuth();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});
