import Config from '@/config';

export default {
  getAbsolutePath(imagePath) {
    return `${Config.getHostName()}${imagePath}`;
  }
};
