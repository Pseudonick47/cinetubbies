import store from 'Store';

import PropsService from 'Api/props.service';

export default {
  requestOfficialProps(theater, page) {
    const num = 9;
    PropsService.fetchOfficialProps(theater, num, page).then((response) => {
      store.commit('props/official/setProps', response.data);
    });
  },

  requestOfficialPropCount(theater) {
    PropsService.fetchOfficialPropsCount(theater).then((response) => {
      store.commit('props/official/setCount', response.data);
    });
  },

  requestCategories() {
    PropsService.fetchCategories().then((response) => {
      store.commit('props/categories/setCategory', response.data);
    });
  }
};
