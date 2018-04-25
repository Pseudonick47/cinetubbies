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
  updateInfo(data) {
    return MoviesApiService.updateInfo(data);
  }
};
