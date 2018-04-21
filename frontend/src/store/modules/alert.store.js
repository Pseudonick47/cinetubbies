const state = {
  showAlert: false,
  alertMessage: '',
  alertColor: 'primary',
  alertIcon: ''
};

const getters = {
  alertIcon: (state) => state.alertIcon,
  alertColor: (state) => state.alertColor,
  alertMessage: (state) => state.alertMessage,
  showAlert: (state) => state.showAlert
};

const mutations = {
  success(state, message) {
    state.alertIcon = 'check_circle';
    state.alertColor = 'success';
    state.alertMessage = message;
    state.showAlert = true;
  },
  info(state, message) {
    state.alertIcon = 'info';
    state.alertColor = 'info';
    state.alertMessage = message;
    state.showAlert = true;
  },
  warning(state, message) {
    state.alertIcon = 'priority_high';
    state.alertColor = 'warning';
    state.alertMessage = message;
    state.showAlert = true;
  },
  error(state, message) {
    state.alertIcon = 'warning';
    state.alertColor = 'error';
    state.alertMessage = message;
    state.showAlert = true;
  },
  turnOff(state) {
    state.showAlert = false;
  }
};

export {
  state,
  getters,
  mutations
};
