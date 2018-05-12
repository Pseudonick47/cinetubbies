import ImageHelper from '@/helpers/image-helper';

const THEATER_KIND = {
  CINEMA: 'm',
  THEATER: 'p'
};

export class Theater {
  constructor(data) {
    this.name = '';
    this.address = '';
    this.kind = '';
    this.description = '';
    this.rating = null;
    _.assignWith(this, data);

    if (this.image) {
      this.image.path = ImageHelper.getAbsolutePath(this.image.path);
    }
  }

  isCinema() {
    return this.kind === THEATER_KIND.CINEMA;
  }

  isTheater() {
    return this.kind === THEATER_KIND.THEATER;
  }

  isRatingNull() {
    return this.rating === null;
  }
}
