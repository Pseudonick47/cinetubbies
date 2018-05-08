import Axios from 'axios';

const USER = 'users/';
const PROPS = 'props/';
const USED = 'used/';
const COUNT = 'count';

const props = {
  fetch(num, page) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}`);
  },

  fetchByUser(num, page, user) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}`);
  },

  fetchByCategory(num, page, category) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}&category=${category}`);
  },

  fetchByUserAndCategory(num, page, user, category) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}&category=${category}`);
  },

  post(data) {
    return Axios.post(`${PROPS}${USED}`, data);
  }
};

const count = {
  fetch() {
    return Axios.get(`${PROPS}${USED}${COUNT}`);
  },

  fetchByUser(user) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}`);
  },

  fetchByCategory(category) {
    return Axios.get(`${PROPS}/${USED}${COUNT}?category=${category}`);
  },

  fetchByUserAndCategory(user, category) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}?category=${category}`);
  }
};

export {
  props,
  count
};
