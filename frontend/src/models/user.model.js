import * as _ from 'lodash';

const USER_ROLES = {
  ADMIN: 'admin',
  CINEMA_ADMIN: 'cinema_admin',
  FAN_ZONE_ADMIN: 'fan_zone_admin',
  USER: 'user'
};

export class User {
  constructor(data) {
    _.assignWith(this, data);
  }

  static get USER_ROLES() {
    return USER_ROLES;
  }

  isAnyAdmin() {
    return this.role === USER_ROLES.ADMIN || this.role === USER_ROLES.CINEMA_ADMIN || this.role === USER_ROLES.FAN_ZONE_ADMIN;
  }

  isAdmin() {
    return this.role === USER_ROLES.ADMIN;
  }

  isCinemaAdmin() {
    return this.role === USER_ROLES.CINEMA_ADMIN;
  }

  isFanZoneAdmin() {
    return this.role === USER_ROLES.FAN_ZONE_ADMIN;
  }
}
