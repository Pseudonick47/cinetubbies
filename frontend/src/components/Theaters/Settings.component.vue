<template>
  <v-layout row>
    <v-flex
      xs-12
      sm5
    >
      <v-chip
        color="white"
        text-color="black">
        <v-icon left>build</v-icon>
        Theater settings
      </v-chip>
      <v-chip
        color="white"
        text-color="black">
        <span v-if="theater.isCinema()">Type: cinema</span>
        <span v-else>Type: theater</span>
        <v-tooltip right>
          <v-icon
            slot="activator"
            right
          >info</v-icon>
          <span>Types: cinema, theater</span>
        </v-tooltip>
      </v-chip>
      <form>
        <v-text-field
          v-model="theater.name"
          label="Name"
        />
        <v-text-field
          v-model="theater.address"
          label="Address"
        />
        <v-text-field
          v-model="theater.description"
          label="Description"
        />
        <v-btn @click="confirmSubmit = true">submit</v-btn>
      </form>
      <v-dialog
        v-model="confirmSubmit"
        persistent
        max-width="300px"
      >
        <v-card>
          <v-card-text>
            Submit changes?
          </v-card-text>
          <v-card-actions>
            <v-btn @click="submit">yes</v-btn>
            <v-spacer/>
            <v-btn @click="confirmSubmit = false">no</v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>
    </v-flex>
    <v-layout column>
      <v-flex
        xs-12
        offset-lg1
      >
        Theater repertoire:
        <v-data-table
          :items="repertoire"
          :headers="headers"
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ getMovie(props.item.movie).title }}</td>
            <td>{{ props.item.auditorium }} </td>
            <td>{{ props.item.date }}</td>
            <td>{{ props.item.time }}</td>
            <td>{{ props.item.price }}</td>
          </template>
          <template slot="no-data">
            Sorry, nothing to display here.
          </template>
        </v-data-table>
      </v-flex>
      <v-flex
        xs-12
        offset-lg1
      >
        Tickets on sale:
        <v-data-table
          :items="tickets"
          :headers="ticketsHeaders"
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ getMovie(getShowtime(props.item.showtime).movie).title }}</td>
            <td>{{ getShowtime(props.item.showtime).auditorium }} </td>
            <td>{{ props.item.seat }} </td>
            <td>{{ getShowtime(props.item.showtime).date }}</td>
            <td>{{ getShowtime(props.item.showtime).time }}</td>
            <td>{{ getShowtime(props.item.showtime).price }}</td>
            <td>{{ props.item.discount }}</td>
          </template>
          <template slot="no-data">
            Sorry, nothing to display here.
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
import SysAdminController from 'Controllers/system-admin.controller';
import TheatersController from 'Controllers/theaters.controller';
import { mapGetters } from 'vuex';
import { Theater } from 'Models/theater.model';
import { Showtime } from 'Models/showtime.model';
import { TicketOnSale } from 'Models/ticket-on-sale.model';
import { Movie } from 'Models/movie.model';

export default {
  name: 'TheaterSettings',

  data: () => ({
    loading: false,
    confirmSubmit: false,
    theater: new Theater(),
    repertoire: [],
    tickets: [],
    movies: []
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'headers',
      'ticketsHeaders'
    ])
  },
  mounted() {
    this.loadTheater();
  },
  methods: {
    loadTheater() {
      this.loading = true;
      SysAdminController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theater = new Theater(response.data);
          SysAdminController.getMovies(this.theater.id)
            .then((response) => {
              this.movies = _.map(response.data, x => new Movie(x));
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
          TheatersController.getRepertoire(this.theater.id)
            .then((response) => {
              this.repertoire = _.map(response.data, x => new Showtime(x));
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
          TheatersController.getTicketsOnSale(this.theater.id)
            .then((response) => {
              this.tickets = _.map(response.data, x => new TicketOnSale(x));
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    submit() {
      this.confirmSubmit = false;
      let data = _.reduce(this.theater, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      this.$validator.validateAll().then((result) => {
        if (result) {
          SysAdminController.update(data, this.theater.id).then((response) => {
            this.$alert.success('Settings successfully saved');
          }).catch(() => {
            this.$alert.error('Error while saving settings');
          });
          return;
        }
        this.$alert.error('Error while saving settings');
      });
    },
    getMovie(id) {
      return this.movies.find((element) => {
        return element.id === id;
      });
    },
    getShowtime(id) {
      return this.repertoire.find((element) => {
        return element.id === id;
      });
    }
  }
};
</script>
