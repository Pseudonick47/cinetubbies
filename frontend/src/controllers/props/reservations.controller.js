import store from 'Store';
import Service from 'Api/props/reservations.service';

export default {
  requestReservationsByUser(userId) {
    Service.fetchReservationsByUser(userId)
      .then((response) => {
        store.commit('props/reservations/setReservations', response.data);
      });
  },

  reservate(id, data) {
    return Service.postReservation(id, data);
  },

  cancelReservation(userId, id) {
    return Service.deleteReservation(userId, id);
  }
};
