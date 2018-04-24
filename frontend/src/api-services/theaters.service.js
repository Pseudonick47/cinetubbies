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
    Axios.post(PREFIX, data);
  }
};
