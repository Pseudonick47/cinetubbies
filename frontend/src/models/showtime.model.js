export class Showtime {
  constructor(data) {
    this.auditorium = '';
    this.date = '';
    this.time = '';
    this.price = '';
    this.movie = '';
    _.assignWith(this, data);
  }
}
