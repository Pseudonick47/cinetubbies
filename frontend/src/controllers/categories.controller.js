import store from 'Store';

import CategoriesService from 'Api/categories.service';

export default {
  requestCategories() {
    CategoriesService.fetchCategories().then((response) => {
      store.commit('categories/set', response.data);
    });
  }
};
