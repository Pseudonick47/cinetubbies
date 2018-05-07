import TicketsOnSaleApiService from 'Api/tickets-on-sale.service';

export default {
  create(data) {
    return TicketsOnSaleApiService.create(data);
  },
  destroy(data) {
    return TicketsOnSaleApiService.destroy(data);
  },
  retrieve(data) {
    return TicketsOnSaleApiService.retrieve(data);
  },
  update(data, id) {
    return TicketsOnSaleApiService.update(data, id);
  },
  bookTicket(data) {
    return TicketsOnSaleApiService.bookTicket(data);
  }
};
