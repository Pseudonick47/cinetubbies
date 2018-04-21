import Vue from 'vue';
import * as _ from 'lodash';
import Axios from 'axios';

import store from 'Store';
import UsersApiService from 'Api/users.service';

export default {
  updateUserProfile(data, id) {
    return UsersApiService.updateUserProfile(data, id);
  }
};
