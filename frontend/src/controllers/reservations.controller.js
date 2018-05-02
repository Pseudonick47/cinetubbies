import store from 'Store';
import ReservationsService from 'Api/reservations.service';

export default {

  requestRewards() {
    return ReservationsService.fetchRewards().then((response) => {
      store.commit('reservations/setRewards', response.data);
    });
  },

  updateRewards(data) {
    return ReservationsService.putRewards(data);
  }
};
