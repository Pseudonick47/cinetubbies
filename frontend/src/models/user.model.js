import * as _ from 'lodash';

const USER_ROLES = {
  ADMIN1: 'admin1',
  ADMIN2: 'admin2',
  ADMIN3: 'admin3',
  USER: 'user'
};

export class User {
  constructor(data) {
    _.assignWith(this, data);
  }

  static get USER_ROLES() {
    return USER_ROLES;
  }

  isAdmin() {
    return this.role === USER_ROLES.ADMIN1 || this.role === USER_ROLES.ADMIN2 || this.role === USER_ROLES.ADMIN3;
  }
}
