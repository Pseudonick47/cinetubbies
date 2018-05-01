import store from 'Store';

import Service from 'Api/props/official-props.service';

export default {
  requestPage(page, payload) {
    // TODO: grab from store;
    const num = 9;
    Service.fetchProps(num, page, payload || {}).then((response) => {
      store.commit('props/official/setProps', response.data);
    });
  },

  requestCount(payload) {
    Service.fetchCount(payload || {}).then((response) => {
      store.commit('props/official/setCount', response.data);
    });
  },

  postProp(data) {
    return Service.postProp(data);
  }
};
