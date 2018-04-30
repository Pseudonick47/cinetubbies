import Axios from 'axios';

const PREFIX = 'users/';
const ENDPOINTS = {
  PROFILE: '',
  FRIENDS: 'friends/'
};

export default {
  updateUserProfile(data, id) {
    return Axios.patch(`${PREFIX}${ENDPOINTS.PROFILE}${id}/`, data);
  },

  getFriends(id) {
    return Axios.get(`${PREFIX}${id}/${ENDPOINTS.FRIENDS}`);
  },

  getAllUsers() {
    return Axios.get(`${PREFIX}`);
  },

  removeFriend(friendId) {
    return Axios.delete(`${PREFIX}${friendId}/${ENDPOINTS.FRIENDS}`);
  },

  addFriend(friendId) {
    return Axios.post(`${PREFIX}${friendId}/${ENDPOINTS.FRIENDS}`);
  },

  searchFriends(query) {
    return Axios.get(`${PREFIX}${ENDPOINTS.FRIENDS}${query}`);
  }
};
