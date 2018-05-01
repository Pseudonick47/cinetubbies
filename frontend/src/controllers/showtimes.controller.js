import ShowtimesApiService from 'Api/showtimes.service';

export default {
  create(data) {
    return ShowtimesApiService.create(data);
  },
  list() {
    return ShowtimesApiService.list();
  },
  destroy(data) {
    return ShowtimesApiService.destroy(data);
  },
  retrieve(data) {
    return ShowtimesApiService.retrieve(data);
  },
  update(data, id) {
    return ShowtimesApiService.update(data, id);
  }
};
