import Axios from 'axios';

const PREFIX = 'theaters/';

export default {
  fetchTheaters(num, page) {
    return Axios.get(`${PREFIX}?num=${num}&page=${page}`);
  },

  fetchCount() {
    return Axios.get(`${PREFIX}count`);
  },

  postTheater(data) {
    return Axios.post(`${PREFIX}create`, data);
  },

  get_theaters() {
    return Axios.get(PREFIX + 'just-theaters/');
  },

  update_rating(data) {
    return Axios.post(PREFIX + 'rating/', data);
  }

};
