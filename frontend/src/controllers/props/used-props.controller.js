import store from 'Store';

import * as Service from 'Api/props/used-props.service';

export default {

  fetchPage(num, page, payload) {
    const { user, category } = payload;

    if (user && category) {
      return Service.props.fetchByUserAndCategory(num, page, user, category);
    } else if (user) {
      return Service.props.fetchByUser(num, page, user);
    } else if (category) {
      return Service.props.fetchByCategory(num, page, category);
    }

    return Service.props.fetch(num, page);
  },

  requestPage(page, payload = {}) {
    // TODO: page caching
    const num = 9;

    this.fetchPage(num, page, payload).then((response) => {
      store.commit('props/used/setProps', response.data);
    });
  },

  fetchCount(payload) {
    const { user, category } = payload;

    if (user && category) {
      return Service.count.fetchByUserAndCategory(user, category);
    } else if (user) {
      return Service.count.fetchByUser(user);
    } else if (category) {
      return Service.count.fetchByCategory(category);
    }

    return Service.count.fetch();
  },

  requestCount(payload = {}) {
    this.fetchCount(payload).then((response) => {
      store.commit('props/used/setCount', response.data);
    });
  },

  postProp(data) {
    return Service.props.post(data);
  }
};
