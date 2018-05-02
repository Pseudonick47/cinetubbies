import Axios from 'axios';

const PROPS = 'props/';
const CATEGORIES = 'categories/';

export default {
  fetchCategories() {
    return Axios.get(`${PROPS}${CATEGORIES}`);
  }
};
