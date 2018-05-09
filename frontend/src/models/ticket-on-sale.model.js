export class TicketOnSale {
  constructor(data) {
    this.auditorium = '';
    this.date = '';
    this.time = '';
    this.price = '';
    this.movie = '';
    this.theater = '';
    this.showtime = '';
    _.assignWith(this, data);
  }
}
