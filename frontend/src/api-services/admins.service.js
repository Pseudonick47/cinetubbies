import Axios from 'axios';

const PREFIX = 'admins/';

export default {
  fetchAdmins(num, page, role) {
    return Axios.get(`${PREFIX}?role=${role}&num=${num}&page=${page}`);
  },

  fetchCount(role) {
    if (role) {
      return Axios.get(`${PREFIX}count/?role=${role}`);
    } else {
      return Axios.get(`${PREFIX}count`);
    }
  },

  postAdmin(data) {
    return Axios.post(PREFIX, data);
  }
};
