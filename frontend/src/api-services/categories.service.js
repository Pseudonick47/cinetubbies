import Axios from 'axios';

const PREFIX = 'fan-zone/';
const CATEGORIES = 'categories/';

export default {
  fetchCategories() {
    return Axios.get(`${PREFIX}${CATEGORIES}`);
  }
};
