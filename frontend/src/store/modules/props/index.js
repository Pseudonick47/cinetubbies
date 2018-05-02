import * as categories from './categories.store';
import * as official from './official-props.store';

export default {
  namespaced: true,
  modules: {
    categories,
    official
  }
};
