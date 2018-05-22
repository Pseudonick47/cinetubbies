import store from 'Store';

import * as Service from 'Api/props/used-props.service';

export default {

  fetchPageForAll(num, page, payload) {
    const { user, category } = payload;

    if (user && category) {
      return Service.props.fetchByUserAndCategoryAll(num, page, user, category);
    } else if (user) {
      return Service.props.fetchByUserAll(num, page, user);
    } else if (category) {
      return Service.props.fetchByCategoryAll(num, page, category);
    }

    return Service.props.fetchAll(num, page);
  },

  fetchPage(num, page, payload) {
    const { user, category, approved } = payload;
    if (user && category) {
      return Service.props.fetchByUserAndCategory(num, page, user, category, approved);
    } else if (user) {
      return Service.props.fetchByUser(num, page, user, approved);
    } else if (category) {
      return Service.props.fetchByCategory(num, page, category, approved);
    }

    return Service.props.fetch(num, page, approved);
  },

  requestPage(page, payload = {}) {
    // TODO: page caching
    const num = 9;

    if (payload.all) {
      this.fetchPageForAll(num, page, payload).then((response) => {
        store.commit('props/setProps', response.data);
      });
    } else {
      this.fetchPage(num, page, payload).then((response) => {
        store.commit('props/setProps', response.data);
      });
    }
  },

  fetchCountForAll(payload) {
    const { user, category } = payload;

    if (user && category) {
      return Service.count.fetchByUserAndCategoryAll(user, category);
    } else if (user) {
      return Service.count.fetchByUserAll(user);
    } else if (category) {
      return Service.count.fetchByCategoryAll(category);
    }

    return Service.count.fetchAll();
  },

  fetchCount(payload) {
    const { user, category, approved } = payload;

    if (user && category) {
      return Service.count.fetchByUserAndCategory(user, category, approved);
    } else if (user) {
      return Service.count.fetchByUser(user, approved);
    } else if (category) {
      return Service.count.fetchByCategory(category, approved);
    }

    return Service.count.fetch(approved);
  },

  requestCount(payload = {}) {
    if (payload.all) {
      this.fetchCountForAll(payload).then((response) => {
        store.commit('props/setCount', response.data);
      });
    } else {
      this.fetchCount(payload).then((response) => {
        store.commit('props/setCount', response.data);
      });
    }
  },

  postProp(data) {
    return Service.props.post(data);
  },

  reviewProp(id, data) {
    return Service.props.review(id, data);
  },

  deleteProp(id) {
    return Service.props.delete(id);
  }
};
