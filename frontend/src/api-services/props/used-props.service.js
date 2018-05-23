import Axios from 'axios';

const USER = 'users/';
const PROPS = 'props/';
const USED = 'used/';
const COUNT = 'count';

const props = {
  fetch(num, page, approved) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}&approved=${approved}`);
  },

  fetchAll(num, page) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}&all=true`);
  },

  fetchByUser(num, page, user, approved) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}&approved=${approved}`);
  },

  fetchByUserAll(num, page, user) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}&all=true`);
  },

  fetchByCategory(num, page, category, approved) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}&category=${category}&approved=${approved}`);
  },

  fetchByCategoryAll(num, page, category) {
    return Axios.get(`${PROPS}${USED}?num=${num}&page=${page}&category=${category}&all=true`);
  },

  fetchByUserAndCategory(num, page, user, category, approved) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}&category=${category}&approved=${approved}`);
  },

  fetchByUserAndCategoryAll(num, page, user, category) {
    return Axios.get(`${USER}${user}/${PROPS}?num=${num}&page=${page}&category=${category}&all=true`);
  },

  post(data) {
    return Axios.post(`${PROPS}${USED}`, data);
  },

  review(id, data) {
    return Axios.put(`${PROPS}${USED}${id}/review`, data);
  },

  delete(id) {
    return Axios.delete(`${PROPS}${USED}${id}`);
  },

  put(id, data) {
    return Axios.put(`${PROPS}${USED}${id}`, data);
  }
};

const count = {
  fetch(approved) {
    return Axios.get(`${PROPS}${USED}${COUNT}?approved=${approved}`);
  },

  fetchAll() {
    return Axios.get(`${PROPS}${USED}${COUNT}&all=true`);
  },

  fetchByUser(user, approved) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}?approved=${approved}`);
  },

  fetchByUserAll(user) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}?all=true`);
  },

  fetchByCategory(category, approved) {
    return Axios.get(`${PROPS}${USED}${COUNT}?category=${category}&approved=${approved}`);
  },

  fetchByCategoryAll(category) {
    return Axios.get(`${PROPS}${USED}${COUNT}?category=${category}&all=true`);
  },

  fetchByUserAndCategory(user, category, approved) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}?category=${category}&approved=${approved}`);
  },

  fetchByUserAndCategoryAll(user, category) {
    return Axios.get(`${USER}${user}/${PROPS}${COUNT}?category=${category}&all=true`);
  }
};

export {
  props,
  count
};
