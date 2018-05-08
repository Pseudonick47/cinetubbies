import { Category } from 'Models/category.model';

const namespaced = true;

const state = {
  data: {}
};

const getters = {
  all: (state) => _.values(state.data),
  one: (state) => (id) => state.data[id],
  subcategories: (state) => (id) => state.data[id].subcategories,
  roots: (state) => _.filter(_.values(state.data), [ 'supercategory', null ]),
  leafs: (state) => _.filter(_.values(state.data), (cat) => _.isEmpty(cat.subcategories))
};

const mutations = {
  setCategories(state, categories) {
    state.data = _.stubObject();

    _.each(_.sortBy(categories, 'id'), (category) => {
      const c = new Category(category);

      if (c.supercategory) {
        state.data[c.supercategory].subcategories.push(c);
      }

      const p = [];
      p.push(c.name);

      let s = c;
      while (s.supercategory) {
        s = state.data[s.supercategory];
        p.push(s.name);
      }

      c.path = _.join(_.reverse(p), ' / ');

      state.data[c.id] = c;
    });
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
