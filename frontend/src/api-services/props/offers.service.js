import Axios from 'axios';

const USERS = 'users/';
const PROPS = 'props/';
const USED = 'used/';
const OFFERS = 'offers/';

export default {
  getOffersByUser(id) {
    return Axios.get(`${USERS}${id}/${OFFERS}`);
  },

  postOffer(id, data) {
    return Axios.post(`${PROPS}${USED}${id}/${OFFERS}`, data);
  },

  putOffer(userId, offerId, data) {
    return Axios.put(`${USERS}${userId}/${OFFERS}${offerId}`, data);
  },

  deleteOffer(userId, id) {
    return Axios.delete(`${USERS}${userId}/${OFFERS}${id}`);
  }
};
