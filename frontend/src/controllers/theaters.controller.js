import store from 'Store';

import TheatersService from 'Api/theaters.service';

export default {
  requestPage(page) {
    const num = store.getters.entriesPerPage;
    TheatersService.fetchTheaters(num, page).then((response) => {
      console.log(response.data);
      store.commit('setTheaters', response.data);
      store.commit('setPage', page);
    });
  },

  requestTheaterCount() {
    TheatersService.fetchCount().then((response) => {
      store.commit('setCount', response.data);
    });
  },

  setEntriesPerPage(num) {
    store.commit('setEntriesPerPage', num);
  },

  registerNewTheater(theater) {
    TheatersService.postTheater(theater).then((response) => {
      this.requestPage(store.getters.page);
    });
  },

  get_theaters() {
    return TheatersService.get_theaters();
  },

  update_rating(data) {
    return TheatersService.update_rating(data);
  }

};
