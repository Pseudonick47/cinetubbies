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

  updateRating(data, id) {
    return Axios.post(`${PREFIX}${id}/rating`, data);
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
  },

  getTicketsOnSale(data) {
    return Axios.get(`${PREFIX}${data}/tickets-on-sale`);
  },

  getRevenue(id, data) {
    return Axios.post(`${PREFIX}${id}/revenue`, data);
  },

  getAuditoriums(theaterId) {
    return Axios.get(`${PREFIX}${theaterId}/auditoriums`);
  },

  retrieveAuditorium(theaterId, auditoriumId) {
    return Axios.get(`${PREFIX}${theaterId}/auditoriums/${auditoriumId}`);
  },

  createAuditorium(theaterId, data) {
    return Axios.post(`${PREFIX}${theaterId}/auditoriums`, data);
  },

  updateAuditorium(theaterId, data) {
    return Axios.put(`${PREFIX}${theaterId}/auditoriums/${data.id}`, data);
  },

  deleteAuditorium(theaterId, auditoriumId) {
    return Axios.delete(`${PREFIX}${theaterId}/auditoriums/${auditoriumId}`);
  }
};
