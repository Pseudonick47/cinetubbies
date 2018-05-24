import Axios from 'axios';

const USERS = 'users/';
const PROPS = 'props/';
const OFFICIAL = 'official/';
const RESERVATIONS = 'reservations/';

export default {
  fetchReservationsByUser(id) {
    return Axios.get(`${USERS}${id}/${RESERVATIONS}`);
  },

  postReservation(id, data) {
    return Axios.post(`${PROPS}${OFFICIAL}${id}/${RESERVATIONS}`, data);
  },

  deleteReservation(userId, id) {
    return Axios.delete(`${USERS}${userId}/${RESERVATIONS}${id}`);
  },

  putReservation(userId, id, data) {
    return Axios.put(`${USERS}${userId}/${RESERVATIONS}${id}`, data);
  }
};
