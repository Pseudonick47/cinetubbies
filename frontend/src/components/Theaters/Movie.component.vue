<template>
  <div>
    <v-parallax
      src="http://blog.hdwallsource.com/wp-content/uploads/2017/05/fast-and-furious-8-logo-wallpaper-61267-63082-hd-wallpapers.jpg"
      class="paralax-kill-margins"
    >
      <v-layout
        column
        align-center
        justify-center>
        <h1 class="white--text title-text-shadow">{{ movie.title }}</h1>
        <h4 class="white--text title-text-shadow">by <i>{{ movie.director }}</i></h4>
      </v-layout>
    </v-parallax>
    <v-layout
      row
      class="my-3"
    >
      <v-flex md5>
        <h3>Title:</h3><p>{{ movie.title }}</p>
        <h3>Director:</h3> <p>{{ movie.director }}</p>
        <h3>Genre:</h3> <p>{{ movie.genre }}</p>
        <h3>Duration:</h3> <p>{{ movie.duration }}</p>
        <h3>Actors:</h3><p>{{ movie.actors }}</p>
        <h3>Description:</h3><p>{{ movie.description }}</p>
        <h3>Rating:</h3> <p>{{ movie.rating || 'Not rated' }}</p>
      </v-flex>

      <v-flex md3>
        <v-date-picker
          v-model="selectedDate"
          :events="showtimeDates"
          full-width
          class="mx-3"
        />
      </v-flex>
      <v-flex md4>
        <v-data-table
          :items="selectedDateShowtimes"
          :total-items="showtimes.length"
          hide-headers
          hide-actions
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ props.item.auditorium }}</td>
            <td class="text-xs-right">{{ props.item.price }}</td>
            <td class="text-xs-right">{{ props.item.time }}</td>
            <td class="text-xs-right">{{ props.item.date }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                icon
                class="mx-0"
                @click="openSeatsDialog(props.item.id)">
                <v-icon color="teal">weekend</v-icon>
              </v-btn>
            </td>
          </template>
          <template slot="no-results">
            <td class="text-xs-center">
              No showtimes for selected date
            </td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
    <book-ticket-dialog
      v-if="showBookDialog"
      :show.sync="showBookDialog"
      :showtime-id="selectedShowtimeId"
      @cancel="closeBookingDialog"
      @book-ticket="bookTicket"
    />
  </div>
</template>

<script>
import * as _ from 'lodash';
import BookTicketDialog from 'Components/Theaters/BookTicketDialog.component';
import MovieController from 'Controllers/movies.controller';
import TicketsOnSaleController from 'Controllers/tickets-on-sale.controller';
import { Movie } from 'Models/movie.model';

export default {
  name: 'Movie',
  components: {
    BookTicketDialog
  },
  props: {
    theaterId: {
      type: String,
      required: true
    },
    movieId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showBookDialog: false,
      selectedShowtimeId: -1,
      selectedDate: null,
      movie: {},
      showtimes: []
    };
  },
  computed: {
    selectedDateShowtimes() {
      return _.filter(this.showtimes, { date: this.selectedDate });
    },
    showtimeDates() {
      return _.map(this.showtimes, (showtime) => {
        return showtime.date;
      });
    }
  },
  mounted() {
    this.getMovie(this.movieId);
    this.getShowtimes(this.movieId);
  },
  methods: {
    openSeatsDialog(showtimeId) {
      this.selectedShowtimeId = showtimeId;
      this.showBookDialog = true;
    },
    closeBookingDialog() {
      this.showBookDialog = false;
    },
    bookTicket(choosenSeats) {
      TicketsOnSaleController.bookTicket({
        choosenSeats,
        showtime: this.selectedShowtimeId
      })
        .then((response) => {
          this.$alert.success('Ticket successfully booked');
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
      this.showBookDialog = false;
    },
    getMovie(id) {
      MovieController.retrieve(id)
        .then((response) => {
          this.movie = new Movie(response.data);
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getShowtimes(id) {
      MovieController.getShowtimes(id)
        .then((response) => {
          this.showtimes = response.data;
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>

<style>
.title-text-shadow {
    text-shadow: 2px 2px 3px #555;
}

.paralax-kill-margins {
  margin-top: -20px;
  margin-left: -16px;
  margin-right: -16px;
}
</style>
