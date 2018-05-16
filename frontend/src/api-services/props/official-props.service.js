import Axios from 'axios';

const THEATERS = 'theaters/';
const PROPS = 'props/';
const OFFICIAL = 'official/';
const CATEGORIES = 'categories/';
const COUNT = 'count';

const props = {
  fetch(num, page) {
    return Axios.get(`${PROPS}${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchByTheater(num, page, theater) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchByCategory(num, page, category) {
    return Axios.get(`${PROPS}${CATEGORIES}${category}/${OFFICIAL}?num=${num}&page=${page}`);
  },

  fetchByTheaterAndCategory(num, page, theater, category) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${CATEGORIES}${category}/${OFFICIAL}?num=${num}&page=${page}`);
  },

  post(data) {
    return Axios.post(`${PROPS}${OFFICIAL}`, data);
  },

  put(id, data) {
    return Axios.put(`${PROPS}${OFFICIAL}${id}`, data);
  },

  delete(id) {
    return Axios.delete(`${PROPS}${OFFICIAL}${id}`);
  }
};

const count = {
  fetch() {
    return Axios.get(`${PROPS}${OFFICIAL}${COUNT}`);
  },

  fetchByTheater(theater) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${OFFICIAL}${COUNT}`);
  },

  fetchByCategory(category) {
    return Axios.get(`${PROPS}${CATEGORIES}${category}/${OFFICIAL}${COUNT}`);
  },

  fetchByTheaterAndCategory(theater, category) {
    return Axios.get(`${THEATERS}${theater}/${PROPS}${CATEGORIES}${category}/${OFFICIAL}${COUNT}`);
  }
};

export {
  props,
  count
};
