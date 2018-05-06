import Axios from 'axios';

const ENDPOINTS = {
  TICKETS: 'sale/'
};

export default {
  create(data) {
    return Axios.post(ENDPOINTS.TICKETS, data);
  },
  destroy(data) {
    return Axios.delete(`${ENDPOINTS.TICKETS}${data}/`);
  },
  retrieve(data) {
    return Axios.get(`${ENDPOINTS.TICKETS}${data}/`);
  },
  update(data, id) {
    return Axios.put(`${ENDPOINTS.TICKETS}${id}/`, data);
  }
};
