
import store from 'Store';
import * as _ from 'lodash';

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
  },

  createAuditorium(theaterId, data) {
    const newData = _.cloneDeep(data);
    newData.layout = { layout: newData.layout };
    return TheatersApiService.createAuditorium(theaterId, newData);
  },

  deleteAuditorium(theaterId, auditoriumId) {
    return TheatersApiService.deleteAuditorium(theaterId, auditoriumId);
  },

  updateAuditorium(theaterId, data) {
    const newData = _.cloneDeep(data);
    newData.layout = { layout: newData.layout };
    return TheatersApiService.updateAuditorium(theaterId, newData);
  },

  retrieveAuditorium(theaterId, auditoriumId) {
    return TheatersApiService.retrieveAuditorium(theaterId, auditoriumId);
  },

  getAuditoriums(theaterId) {
    return TheatersApiService.getAuditoriums(theaterId);
  },
  mapAuditoriums(data) {
    return _.map(data, x => {
      x.layout = x.layout.layout;
      return x;
    });
  }
};
