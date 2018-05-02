import Axios from 'axios';

const MEDIA = 'media/';
const IMAGES = 'images/';

export default {
  postImage(data) {
    return Axios.post(`${MEDIA}${IMAGES}`, data);
  }
};
