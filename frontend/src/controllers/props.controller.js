import store from 'Store';

import PropsService from 'Api/props.service';

export default {
  requestOfficialProps(page, theater = null) {
    const num = 9;
    if (theater) {
      PropsService.fetchOfficialPropsByTheater(theater, num, page).then((response) => {
        store.commit('props/official/setProps', response.data);
      });
    } else {
      PropsService.fetchOfficialProps(num, page).then((response) => {
        store.commit('props/official/setProps', response.data);
      });
    }
  },

  requestOfficialPropCount(theater = null) {
    if (theater) {
      PropsService.fetchOfficialPropsCountByTheater(theater).then((response) => {
        store.commit('props/official/setCount', response.data);
      });
    } else {
      PropsService.fetchOfficialPropsCount().then((response) => {
        store.commit('props/official/setCount', response.data);
      });
    }
  },

  requestCategories() {
    PropsService.fetchCategories().then((response) => {
      store.commit('props/categories/setCategory', response.data);
    });
  },

  postOfficialProp(data) {
    return PropsService.postOfficialProp(data);
  }
};
