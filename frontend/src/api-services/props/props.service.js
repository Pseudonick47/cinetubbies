import Axios from 'axios';

const PROPS = 'props/';
const COUNT = 'count';

const props = {
  fetch(num, page) {
    return Axios.get(`${PROPS}?num=${num}&page=${page}`);
  },
  fetchByCategory(num, page, category) {
    return Axios.get(`${PROPS}?num=${num}&page=${page}&category=${category}`);
  }
};

const count = {
  fetch() {
    return Axios.get(`${PROPS}${COUNT}`);
  },
  fetchByCategory(category) {
    return Axios.get(`${PROPS}${COUNT}?category=${category}`);
  }
};

export {
  props,
  count
};
