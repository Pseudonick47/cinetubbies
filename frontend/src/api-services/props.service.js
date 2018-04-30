import Axios from 'axios';

const THEATERS = 'theaters/';
const PROPS = 'props/';
const OFFICIAL = 'official/';
const CATEGORIES = 'categories/';

export default {
  fetchOfficialProps(theater, num, page) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchOfficialPropsCount(theater) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}count`);
  },

  fetchCategories() {
    return Axios.get(`${PROPS}${CATEGORIES}`);
  }
};
