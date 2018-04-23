import MoviesApiService from 'Api/movies.service';

export default {
  create(data) {
    return MoviesApiService.create(data);
  },
  list() {
    return MoviesApiService.list();
  },
  destroy(data) {
    return MoviesApiService.destroy(data);
  }
};
