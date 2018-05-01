import Axios from 'axios';

const THEATERS = 'theaters/';
const PROPS = 'props/';
const OFFICIAL = 'official/';
const CATEGORIES = 'categories/';

export default {
  fetchOfficialProps(num, page) {
    return Axios.get(`${PROPS}${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchOfficialPropsCount() {
    return Axios.get(`${PROPS}${OFFICIAL}count`);
  },

  fetchOfficialPropsByTheater(theater, num, page) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchOfficialPropsCountByTheater(theater) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}count`);
  },

  fetchCategories() {
    return Axios.get(`${PROPS}${CATEGORIES}`);
  },

  postOfficialProp(data) {
    return Axios.post(`${PROPS}${OFFICIAL}`, data);
  }
};
