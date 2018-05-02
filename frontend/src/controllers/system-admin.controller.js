import store from 'Store';

import TheatersService from 'Api/theaters.service';
import AdminsService from 'Api/admins.service';

export default {
  requestTheaters(num, page) {
    TheatersService.fetchTheaters(num, page).then((response) => {
      store.commit('systemAdmin/setData', response.data);
      store.commit('systemAdmin/setPage', page);
    });
  },

  requestAdmins(num, page, role) {
    AdminsService.fetchAdmins(num, page, role).then((response) => {
      store.commit('systemAdmin/setData', response.data);
      store.commit('systemAdmin/setPage', page);
    });
  },

  requestPage(page, kind) {
    const num = store.getters['systemAdmin/entriesPerPage'];
    if (kind === 'theaters') {
      this.requestTheaters(num, page);
    } else if (kind === 'theater-admins') {
      this.requestAdmins({ num, page, role: 'cinema_admin' });
    } else {
      this.requestAdmins({ num, page, role: 'fan_zone_admin' });
    }
  },

  requestCount(kind) {
    if (kind === 'theaters') {
      TheatersService.fetchCount().then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    } else if (kind === 'theater-admins') {
      AdminsService.fetchCount('cinema_admin').then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    } else {
      AdminsService.fetchCount('fan_zone_admin').then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    }
  },

  requestAdminsTheater(id) {
    return AdminsService.fetchAdminsTheater(id).then((response) => {
      store.commit('setAdminsTheater', response.data);
    });
  },

  requestTheaterAdmins() {
    AdminsService.fetchAdmins({ role: 'cinema_admin', all: true })
      .then((response) => {
        store.commit('systemAdmin/setTheaterAdmins', response.data);
      });
  },

  setEntriesPerPage(num) {
    store.commit('systemAdmin/setEntriesPerPage', num);
  },

  registerTheater(theater) {
    return TheatersService.postTheater(theater);
  },

  registerAdmin(admin, kind) {
    AdminsService.postAdmin(admin).then((response) => {
      this.requestCount(kind);
      this.requestPage(store.getters['systemAdmin/page'], kind);
    });
  },

  getTheaters() {
    return TheatersService.getTheaters();
  },

  updateRating(data) {
    return TheatersService.updateRating(data);
  },

  getTheater(data) {
    return TheatersService.getTheater(data);
  },

  update(data, id) {
    return TheatersService.update(data, id);
  },

  getMovies(data) {
    return TheatersService.getMovies(data);
  }
};
