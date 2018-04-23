import Axios from 'axios';

const PREFIX = 'users/';
const ENDPOINTS = {
  PROFILE: ''
};

export default {
  updateUserProfile(data, id) {
    return Axios.patch(`${PREFIX}${ENDPOINTS.PROFILE}${id}/`, data);
  }
};
