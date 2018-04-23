import UsersApiService from 'Api/users.service';
import store from 'Store';

export default {
  updateUserProfile(data, id) {
    return UsersApiService.updateUserProfile(data, id).then(({ data }) => {
      store.commit('updateActiveUser', data);
      localStorage.setItem('user', JSON.stringify(data));
    });
  }
};
