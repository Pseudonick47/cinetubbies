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
      // TODO: rename role
      this.requestAdmins(num, page, 'cinema_admin');
    } else {
      this.requestAdmins(num, page, 'fan_zone_admin');
    }
  },

  requestCount(kind) {
    if (kind === 'theaters') {
      TheatersService.fetchCount().then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    } else if (kind === 'theaters-admin') {
      AdminsService.fetchCount('cinema_admin').then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    } else {
      AdminsService.fetchCount('fan_zone_admin').then((response) => {
        store.commit('systemAdmin/setCount', response.data);
      });
    }
  },

  setEntriesPerPage(num) {
    store.commit('systemAdmin/setEntriesPerPage', num);
  },

  registerNewTheater(theater) {
    TheatersService.postTheater(theater).then((response) => {
      this.requestPage(store.getters['systemAdmin/page']);
    });
  },

  registerNewAdmin(admin) {
    AdminsService.postAdmin(admin).then((response) => {
      this.requestPage(store.getters['systemAdmin/page']);
    });
  }
};
