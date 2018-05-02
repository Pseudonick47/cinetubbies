<template>
  <div>
    <v-jumbotron
      gradient="to top right, rgba(63,81,181, .7), rgba(25,32,72, .7)"
      src="https://wasahiro.files.wordpress.com/2014/02/sharknado-2-banner.png"
      dark
    >
      <v-container fill-height>
        <v-layout align-center>
          <v-flex text-xs-center>
            <h3 class="display-3">{{ movie.title }}</h3>
          </v-flex>
        </v-layout>
      </v-container>
    </v-jumbotron>
    <v-layout
      row
    >
      <v-flex xs6>
        Here comes the movie info
      </v-flex>

      <v-flex xs6>
        <v-date-picker
          v-model="date"
          full-width
          landscape
          class="mt-3"
        />
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import MovieController from 'Controllers/movies.controller';
import { Movie } from 'Models/movie.model';

export default {
  name: 'Movie',
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
      date: null,
      loading: false,
      movie: {},
      showtimes: []
    };
  },
  mounted() {
    this.getMovie(this.movieId);
    this.getShowtimes(this.movieId);
  },
  methods: {
    getMovie(id) {
      MovieController.retrieve(id)
        .then((response) => {
          this.movie = new Movie(response.data);
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    getShowtimes(id) {
      MovieController.getShowtimes(id)
        .then((response) => {
          this.showtimes = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
