import store from 'Store';

import * as Service from 'Api/props/official-props.service';

export default {

  fetchPage(num, page, payload) {
    const { theater, category } = payload;

    if (theater && category) {
      return Service.props.fetchByTheaterAndCategory(num, page, theater, category);
    } else if (theater) {
      return Service.props.fetchByTheater(num, page, theater);
    } else if (category) {
      return Service.props.fetchByCategory(num, page, category);
    }

    return Service.props.fetch(num, page);
  },

  requestPage(page, payload = {}) {
    // TODO: page caching
    const num = 9;

    this.fetchPage(num, page, payload).then((response) => {
      store.commit('props/setProps', response.data);
    });
  },

  fetchCount(payload) {
    const { theater, category } = payload;

    if (theater && category) {
      return Service.count.fetchByTheaterAndCategory(theater, category);
    } else if (theater) {
      return Service.count.fetchByTheater(theater);
    } else if (category) {
      return Service.count.fetchByCategory(category);
    }

    return Service.count.fetch();
  },

  requestCount(payload = {}) {
    this.fetchCount(payload).then((response) => {
      store.commit('props/setCount', response.data);
    });
  },

  createProp(data) {
    return Service.props.post(data);
  },

  updateProp(id, data) {
    return Service.props.put(id, data);
  },

  deleteProp(id) {
    return Service.props.delete(id);
  }
};
