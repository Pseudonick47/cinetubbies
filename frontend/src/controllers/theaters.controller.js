
import TheatersApiService from 'Api/theaters.service';

export default {

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
