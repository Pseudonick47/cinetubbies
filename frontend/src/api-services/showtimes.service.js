import Axios from 'axios';

const ENDPOINTS = {
  SHOWTIMES: 'showtimes/'
};

export default {
  create(data) {
    return Axios.post(ENDPOINTS.SHOWTIMES, data);
  },
  list() {
    return Axios.get(ENDPOINTS.SHOWTIMES);
  },
  destroy(data) {
    return Axios.delete(`${ENDPOINTS.SHOWTIMES}${data}/`);
  },
  retrieve(data) {
    return Axios.get(`${ENDPOINTS.SHOWTIMES}${data}/`);
  },
  update(data, id) {
    return Axios.put(`${ENDPOINTS.SHOWTIMES}${id}/`, data);
  }
};
