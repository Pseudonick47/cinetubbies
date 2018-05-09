import ImageHelper from '@/helpers/image-helper';

export class Movie {
  constructor(data) {
    this.title = '';
    this.genre = '';
    this.director = '';
    this.actors = '';
    this.duration = '';
    this.description = '';
    this.theater = '';
    _.assignWith(this, data);

    if (this.image) {
      this.image.path = ImageHelper.getAbsolutePath(this.image.path);
    }
  }
}
