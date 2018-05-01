import { OfficialProp } from 'Models/props/official-prop.model';
import ImageHelper from '@/helpers/image-helper';

const namespaced = true;

const state = {
  props: [],
  count: 0
};

const getters = {
  all: (state) => state.props,
  one: (state) => (id) => _.find(state.props, 'id'),
  count: (state) => state.count
};

const mutations = {
  setProps(state, props) {
    state.props = [];
    _.forEach(props, (prop) => {
      if (prop.image) {
        console.log(ImageHelper.getAbsolutePath('/media/default/theater.jpg'));
        prop.image.path = ImageHelper.getAbsolutePath(prop.image.path);
      }
      state.props.push(new OfficialProp(prop));
    });
  },

  setCount(state, count) {
    state.count = count;
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
