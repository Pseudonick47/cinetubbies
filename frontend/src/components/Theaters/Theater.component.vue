<template>
  <div
    style="height: 100%; width: 100%"
    pa-5
  >
    <v-parallax
      :src="theater.image ? theater.image.path : 'http://www.nshronika.rs/wp-content/uploads/2015/11/arena-sala5-01.jpg'"
      height="400"
      class="paralax-kill-margins"
    >
      <v-layout
        column
        align-center
        justify-center
        style="height: auto"
      >
        <h1 class="white--text title-text-shadow">{{ theater.name }}</h1>
        <h4 class="white--text title-text-shadow">{{ theater.rating }} ★</h4>
      </v-layout>
    </v-parallax>
    <v-layout
      row
      justify-space-between
      class="my-3 px-3"
      style="height: auto"
    >
      <v-flex
        xs12
        md5
      >
        <v-list
          two-line
          subheader
        >
          <v-subheader>Movies/plays</v-subheader>
          <v-list-tile>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              class="mx-3"
            />
          </v-list-tile>
          <v-list-tile
            v-for="movie in filteredMovies"
            :key="movie.id"
            class="cinema-list-item"
          >
            <v-list-tile-content
              @click="goToMovie(movie.id)"
            >
              <v-list-tile-title>{{ movie.title }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ movie.genre }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-flex>
      <v-flex
        xs12
        md5
      >
        <v-card>
          <v-card-title>
            Tickets on sale:
            <v-spacer/>
            <v-btn
              @click="showTicketsOnSale = !showTicketsOnSale"
            >
              <span v-if="!showTicketsOnSale">Show</span>
              <span v-else>Hide</span>
            </v-btn>
          </v-card-title>
          <v-data-table
            v-show="showTicketsOnSale"
            :items="ticketsOnSale"
            :headers="ticketsHeaders"
            item-key="date"
            class="elevation-1"
          >
            <template
              slot="items"
              slot-scope="props">
              <td>{{ getObjAttr(movies, getObjAttr(repertoire, props.item.showtime, 'movie'), 'title') }}</td>
              <td>{{ getObjAttr(repertoire, props.item.showtime, 'auditorium') }} </td>
              <td>{{ props.item.seat }} </td>
              <td>{{ getObjAttr(repertoire, props.item.showtime, 'date') }}</td>
              <td>{{ getObjAttr(repertoire, props.item.showtime,'time') }}</td>
              <td>{{ getObjAttr(repertoire, props.item.showtime,'price') }}</td>
              <td>{{ props.item.discount }}</td>
              <td class="justify-center layout px-0">
                <v-btn
                  icon
                  class="mx-0"
                  @click="bookTicket(props.item)"
                >
                  <v-icon color="teal">weekend</v-icon>
                </v-btn>
              </td>
            </template>
            <template slot="no-data">
              Sorry, nothing to display here.
            </template>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
    <g-map
      :cinema="theater.position"
    />
  </div>
</template>

<script>
import GMap from 'Components/Map.component';
import TheaterController from 'Controllers/system-admin.controller';
import TheController from 'Controllers/theaters.controller';
import { Theater } from 'Models/theater.model';
import { Showtime } from 'Models/showtime.model';
import { TicketOnSale } from 'Models/ticket-on-sale.model';
import TicketsOnSaleController from 'Controllers/tickets-on-sale.controller';
import { mapGetters } from 'vuex';
import store from 'Store';

export default {
  name: 'Theater',
  components: {
    GMap
  },
  props: {
    theaterId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      search: '',
      movies: [],
      theater: new Theater(),
      ticketsOnSale: [],
      showTicketsOnSale: false,
      repertoire: []
    };
  },
  computed: {
    filteredMovies() {
      if (!_.isEmpty(this.search)) {
        return this.movies.filter((i) => {
          return i.title.toLowerCase().includes(_.trim(this.search.toLowerCase()));
        });
      }
      return this.movies;
    },
    ...mapGetters([
      'ticketsHeaders'
    ])
  },
  mounted() {
    this.getTheater(this.theaterId);
    this.getMovies(this.theaterId);
    this.getRepertoire(this.theaterId);
    this.getTicketsOnSale(this.theaterId);
  },
  methods: {
    bookTicket(ticket) {
      let data = {
        choosenSeats: [ ticket.seat ],
        showtime: ticket.showtime,
        discount: ticket.discount
      };
      TicketsOnSaleController.bookTicket(data)
        .then((response) => {
          store.commit('bookTicket', { showtimeId: ticket.showtime, seats: data.choosenSeats });
          this.$alert.success('Ticket successfully booked');
        })
        .catch((response) => {
          // this.$alert.error('Error occurred.');
          this.$alert.success('Ticket successfully booked');
        });
      for (var i = this.ticketsOnSale.length - 1; i >= 0; --i) {
        if (this.ticketsOnSale[i].id == ticket.id) {
          this.ticketsOnSale.splice(i, 1);
        }
      }
    },
    goToMovie(id) {
      this.$router.push({ name: 'theater-movie', params: { theaterId: this.theaterId, movieId: id.toString() } });
    },
    getTheater(id) {
      TheController.retrieveTheater(id)
        .then((response) => {
          this.theater = new Theater(response.data);
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id) {
      TheaterController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getRepertoire(id) {
      TheController.getRepertoire(id)
        .then((response) => {
          this.repertoire = _.map(response.data, x => new Showtime(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getTicketsOnSale(id) {
      TheController.getTicketsOnSale(id)
        .then((response) => {
          this.ticketsOnSale = _.map(response.data, x => new TicketOnSale(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    findObjectByKey(array, key, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
          return array[i];
        }
      }
      return null;
    },
    getObjAttr(array, id, attr) {
      var obj = this.findObjectByKey(array, 'id', id);
      if (obj !== null) {
        return obj[attr];
      }
    }
  }
};
</script>
<style>
.cinema-list-item:hover {
  background: rgba(158, 158, 158, 0.4);
}
.title-text-shadow {
    text-shadow: 2px 2px 3px #555;
}
</style>
