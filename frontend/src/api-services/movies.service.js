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
    return Axios.delete(ENDPOINTS.MOVIES + data + '/');
  }
};
