import store from 'Store';

import * as Service from 'Api/props/props.service';

export default {
  requestPage(page, payload = {}) {
    // TODO: page caching
    const num = 9;

    if (payload.category) {
      Service.props.fetchByCategory(num, page, payload.category).then((response) => {
        store.commit('props/setProps', response.data);
      });
    } else {
      Service.props.fetch(num, page).then((response) => {
        store.commit('props/setProps', response.data);
      });
    }
  },

  requestCount(payload = {}) {
    if (payload.category) {
      Service.count.fetchByCategory(payload.category).then((response) => {
        store.commit('props/setCount', response.data);
      });
    } else {
      Service.count.fetch().then((response) => {
        store.commit('props/setCount', response.data);
      });
    }
  }
};
