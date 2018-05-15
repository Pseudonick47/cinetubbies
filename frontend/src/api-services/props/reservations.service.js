import Axios from 'axios';

// const USERS = 'users/';
const PROPS = 'props/';
const OFFICIAL = 'official/';
const RESERVATIONS = 'reservations/';

export default {
  reservate(id, data) {
    return Axios.post(`${PROPS}${OFFICIAL}${id}/${RESERVATIONS}`, data);
  }
};
