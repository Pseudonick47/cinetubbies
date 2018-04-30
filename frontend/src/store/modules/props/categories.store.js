import { Category } from 'Models/category.model';

const namespaced = true;

const state = {
  categories: []
};

const getters = {
  all: (state) => state.categories,
  one: (state) => (id) => _.find(state.categories, 'id'),
  subcategories: (state) => (id) => _.filter(state.categories, [ 'supercategory', id ])
};

const mutations = {
  setCategory(state, categories) {
    state.categories = [];
    _.forEach(categories, (category) => {
      state.categories.push(new Category(category));
    });
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
