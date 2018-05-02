import store from 'Store';

import Service from 'Api/props/categories.service';

export default {
  requestCategories() {
    Service.fetchCategories().then((response) => {
      store.commit('props/categories/setCategories', response.data);
    });
  }
};
