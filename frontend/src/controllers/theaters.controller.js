
import TheatersApiService from 'Api/theaters.service';

export default {

  retrieveTheater(id) {
    return TheatersApiService.retrieveTheater(id);
  }
};
