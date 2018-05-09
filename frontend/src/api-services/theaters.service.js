import Axios from 'axios';

const PREFIX = 'theaters/';

export default {
  fetchTheaters(num, page) {
    return Axios.get(`${PREFIX}?num=${num}&page=${page}`);
  },

  fetchAllTheaters(num, page) {
    return Axios.get(`${PREFIX}?all=true`);
  },

  retrieveTheater(id) {
    return Axios.get(`${PREFIX}${id}`);
  },

  fetchCount() {
    return Axios.get(`${PREFIX}count`);
  },

  postTheater(data) {
    return Axios.post(`${PREFIX}`, data);
  },

  getTheaters() {
    return Axios.get(`${PREFIX}all`);
  },

  updateRating(data) {
    return Axios.post(`${PREFIX}rating`, data);
  },

  // returns theater whose admin is passed through parameter
  getTheater(data) {
    return Axios.get(`${PREFIX}admins/${data}/theater`);
  },

  update(data, id) {
    return Axios.put(`${PREFIX}${id}`, data);
  },

  getMovies(data) {
    return Axios.get(`${PREFIX}${data}/movies`);
  },

  getRepertoire(data) {
    return Axios.get(`${PREFIX}${data}/repertoire`);
  }

};
