import MoviesApiService from 'Api/movies.service';

export default {
  create(data) {
    return MoviesApiService.create(data);
  },
  getMovies() {
    return MoviesApiService.getMovies();
  },
  destroy(data) {
    return MoviesApiService.destroy(data);
  },
  update_info(data) {
    return MoviesApiService.update_info(data);
  },
  retrieve(data) {
    return MoviesApiService.retrieve(data);
  },
  update(data, id) {
    return MoviesApiService.update(data, id);
  }
};
