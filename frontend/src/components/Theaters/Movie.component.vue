<template>
  <div>
    <v-parallax
      src="http://blog.hdwallsource.com/wp-content/uploads/2017/05/fast-and-furious-8-logo-wallpaper-61267-63082-hd-wallpapers.jpg"
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

<style>
.title-text-shadow {
    text-shadow: 2px 2px 3px #555;
}
</style>
