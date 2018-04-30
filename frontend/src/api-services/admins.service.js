import * as _ from 'lodash';
import Axios from 'axios';

const PREFIX = 'admins/';

export default {
  fetchAdmins(params) {
    let urlParams = '?';

    _.forOwn(params, (value, key) => {
      urlParams += `&${key}=${value}`;
    });
    return Axios.get(`${PREFIX}${urlParams}`);
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
