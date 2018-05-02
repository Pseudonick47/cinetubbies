import Axios from 'axios';

const RESERVATIONS = 'reservations/';
const REWARDS = 'rewards/';

export default {
  fetchRewards() {
    return Axios.get(`${RESERVATIONS}${REWARDS}`);
  },

  putRewards(data) {
    return Axios.put(`${RESERVATIONS}${REWARDS}`, data);
  }
};
