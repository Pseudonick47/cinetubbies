import Axios from 'axios';

const PROPS = 'props/';
const COUNT = 'count';

const props = {
  fetch(num, page) {
    return Axios.get(`${PROPS}?num=${num}&page=${page}`);
  },
  fetchByCategory(num, page, category) {
    return Axios.get(`${PROPS}?num=${num}&page=${page}&category=${category}`);
  },
  fetchByTitle(num, page, title) {
    return Axios.get(`${PROPS}?num=${num}&page=${page}&title=${title}`);
  },
  fetchOne(id) {
    return Axios.get(`${PROPS}${id}`);
  }
};

const count = {
  fetch() {
    return Axios.get(`${PROPS}${COUNT}`);
  },
  fetchByCategory(category) {
    return Axios.get(`${PROPS}${COUNT}?category=${category}`);
  },
  fetchByTitle(title) {
    return Axios.get(`${PROPS}${COUNT}?title=${title}`);
  }
};

export {
  props,
  count
};
