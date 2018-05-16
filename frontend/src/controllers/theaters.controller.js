
import store from 'Store';

import TheatersApiService from 'Api/theaters.service';

export default {

  requestAllTheaters() {
    TheatersApiService.fetchAllTheaters().then((response) => {
      store.commit('systemAdmin/setData', response.data);
    });
  },

  retrieveTheater(id) {
    return TheatersApiService.retrieveTheater(id);
  },

  getRepertoire(id) {
    return TheatersApiService.getRepertoire(id);
  },

  getTicketsOnSale(id) {
    return TheatersApiService.getTicketsOnSale(id);
  }

};
