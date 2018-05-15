import Service from 'Api/props/reservations.service';

export default {
  reservate(id, data) {
    return Service.reservate(id, data);
  }
};
