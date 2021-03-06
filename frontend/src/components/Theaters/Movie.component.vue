<template>
  <div>
    <v-dialog
      v-model="showRatingDialog"
      max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Please rate us!</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout
              column>
              <v-flex>
                Theater
                <star-rating
                  :max-rating="5"
                  :star-size="20"
                  inactive-color="#cc99ff"
                  active-color="#9900cc"
                  @rating-selected="setTheaterRating($event)"
                />
              </v-flex>
              <v-flex>
                Movie
                <star-rating
                  :max-rating="5"
                  :star-size="20"
                  inactive-color="#cc99ff"
                  active-color="#9900cc"
                  @rating-selected="setMovieRating($event)"
                />
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-btn @click="showRatingDialog=false">close</v-btn>
        <v-btn @click="showRatingDialog=false">ok</v-btn>
      </v-card>
    </v-dialog>
    <v-parallax
      :src="movie.image ? movie.image.path : 'https://img00.deviantart.net/3a09/i/2017/216/0/4/avengers__infinity_war_wallpaper_by_beyondityart-dbiwtto.jpg'"
      class="paralax-kill-margins"
    >
      <v-layout
        column
        align-center
        justify-center
      >
        <h1 class="white--text title-text-shadow">{{ movie.title }}</h1>
        <h4 class="white--text title-text-shadow">by <i>{{ movie.director }}</i></h4>
      </v-layout>
    </v-parallax>
    <v-layout
      row
      class="my-3"
      px-3
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
      @invite-friends="inviteFriends"
    />
  </div>
</template>

<script>
import * as _ from 'lodash';
import BookTicketDialog from 'Components/Theaters/BookTicketDialog.component';
import MovieController from 'Controllers/movies.controller';
import SysAdminController from 'Controllers/system-admin.controller';
import TicketsOnSaleController from 'Controllers/tickets-on-sale.controller';
import { Movie } from 'Models/movie.model';
import StarRating from 'vue-star-rating';
import store from 'Store';
import { mapGetters } from 'vuex';

export default {
  name: 'Movie',
  components: {
    BookTicketDialog,
    StarRating
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
      showtimes: [],
      showRatingDialog: false
    };
  },
  computed: {
    ...mapGetters([
      'auditorium',
      'auditoriums',
      'showtime'
    ]),
    selectedDateShowtimes() {
      return _.filter(this.showtimes, { date: this.selectedDate });
    },
    selectedShowtime() {
      return _.find(this.showtimes, x => x.id === this.selectedShowtimeId);
    },
    showtimeDates() {
      return _.map(this.showtimes, (showtime) => {
        return showtime.date;
      });
    }
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.getMovie(this.movieId);
      this.getShowtimes(this.movieId);
      store.dispatch('fetchAuditoriums', this.theaterId);
    },
    openSeatsDialog(showtimeId) {
      this.selectedShowtimeId = showtimeId;
      this.showBookDialog = true;
    },
    closeBookingDialog() {
      this.showBookDialog = false;
    },
    mapXYToSeatIds(choosenSeats) {
      const size = this.auditorium(this.selectedShowtime.auditorium).layout[0].length;
      let tmpLayout = _.chunk(this.showtime(this.selectedShowtimeId).seats, size);
      return _.map(choosenSeats, (seatXY) => {
        return tmpLayout[seatXY.x][seatXY.y].seat;
      });
    },
    bookTicket(choosenSeats, mayInviteFriends = false) {
      let data = {
        choosenSeats: this.mapXYToSeatIds(choosenSeats),
        showtime: this.selectedShowtimeId
      };
      TicketsOnSaleController.bookTicket(data)
        .then((response) => {
          store.commit('bookTicket', { showtimeId: this.selectedShowtimeId, seats: data.choosenSeats });
          this.$alert.success('Ticket successfully booked');
          this.showRatingDialog = true;
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
      if (!mayInviteFriends) {
        this.showBookDialog = false;
      }
    },
    inviteFriends(friends, choosenSeats) {
      let seats = this.mapXYToSeatIds(choosenSeats);
      let data = { seats: {} };
      let index = 0;
      _.forEach(friends, friend => {
        data.seats[seats[index++]] = { user: friend };
      });
      TicketsOnSaleController.inviteFriends(this.selectedShowtimeId, data)
        .then((response) => {
          this.$alert.success('Friends successfully invited');
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
          store.commit('setShowtimes', response.data);
          this.showtimes = response.data;
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
    },
    setTheaterRating(rating) {
      const data = { 'rating': rating };
      SysAdminController.updateRating(data, this.theaterId)
        .then((response) => {
          this.$alert.success('Thank you!');
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    setMovieRating(rating) {
      const data = { 'rating': rating, 'id': this.movieId };
      MovieController.updateRating(data, this.movieId)
        .then((response) => {
          this.$alert.success('Thank you!');
        })
        .catch((response) => {
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
