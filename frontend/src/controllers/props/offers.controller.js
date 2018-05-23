import store from 'Store';
import Service from 'Api/props/offers.service';

export default {
  requestOffersByUser(userId) {
    Service.getOffersByUser(userId)
      .then((response) => {
        store.commit('props/offers/set', response.data);
      });
  },

  offer(id, data) {
    return Service.postOffer(id, data);
  },

  deleteOffer(userId, id) {
    return Service.deleteOffer(userId, id);
  },

  updateOffer(userId, offerId, data) {
    return Service.putOffer(userId, offerId, data);
  }
};
