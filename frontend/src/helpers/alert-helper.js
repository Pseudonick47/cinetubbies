import store from 'Store';

export default {
  turnOff() {
    setTimeout(() => {
      store.commit('turnOff');
    }, 5000);
  },

  info(message) {
    store.commit('info', message);
    this.turnOff();
  },

  warning(message) {
    store.commit('warning', message);
    this.turnOff();
  },

  error(message) {
    store.commit('error', message);
    this.turnOff();
  },

  success(message) {
    store.commit('success', message);
    this.turnOff();
  }
};
