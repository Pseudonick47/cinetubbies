import Axios from 'axios';

const ENDPOINTS = {
  MOVIES: 'movies/'
};

export default {
  create(data) {
    return Axios.post(ENDPOINTS.MOVIES, data);
  },
  getMovies() {
    return Axios.get(ENDPOINTS.MOVIES);
  },
  destroy(data) {
    return Axios.delete(`${ENDPOINTS.MOVIES}${data}/`);
  },
  update_info(data) {
    return Axios.patch(ENDPOINTS.MOVIES, data);
  },
  retrieve(data) {
    return Axios.get(`${ENDPOINTS.MOVIES}${data}/`);
  },
  update(data, id) {
    return Axios.put(`${ENDPOINTS.MOVIES}${id}/`, data);
  }
};
