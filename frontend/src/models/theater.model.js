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
    _.assignWith(this, data);
  }

  isCinema() {
    return this.kind === THEATER_KIND.CINEMA;
  }

  isTheater() {
    return this.kind === THEATER_KIND.THEATER;
  }
}
