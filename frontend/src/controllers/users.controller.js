import UsersApiService from 'Api/users.service';

export default {
  updateUserProfile(data, id) {
    return UsersApiService.updateUserProfile(data, id);
  }
};
