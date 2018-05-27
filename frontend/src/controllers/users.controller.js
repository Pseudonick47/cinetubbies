import UsersApiService from 'Api/users.service';
import store from 'Store';

export default {
  updateUserProfile(data, id) {
    return UsersApiService.updateUserProfile(data, id).then(({ data }) => {
      store.commit('updateActiveUser', data);
      localStorage.setItem('user', JSON.stringify(data));
    });
  },

  getProfile(userId) {
    return UsersApiService.getProfile(userId);
  },

  getAllUsers() {
    return UsersApiService.getAllUsers();
  },

  removeFriend(id) {
    return UsersApiService.removeFriend(id);
  },

  addFriend(id) {
    return UsersApiService.addFriend(id);
  },

  searchFriends(query) {
    return UsersApiService.searchFriends(query);
  }
};
