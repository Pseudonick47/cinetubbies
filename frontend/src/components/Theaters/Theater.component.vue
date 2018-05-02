<template>
  <div>
    <v-jumbotron
      gradient="to top right, rgba(63,81,181, .7), rgba(25,32,72, .7)"
      src="http://arab-culture.info/wp-content/uploads/2018/02/1-68.jpg"
      dark
    >
      <v-container fill-height>
        <v-layout align-center>
          <v-flex text-xs-center>
            <h3 class="display-3">{{ theater.name }}</h3>
          </v-flex>
        </v-layout>
      </v-container>
    </v-jumbotron>
    <v-layout row>
      <v-flex>
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
    </v-layout>
  </div>
</template>

<script>
import TheaterController from 'Controllers/system-admin.controller';
import TheController from 'Controllers/theaters.controller';
import { Theater } from 'Models/theater.model';

export default {
  name: 'Theater',
  props: {
    theaterId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      search: '',
      movies: [],
      theater: {}
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
    }
  },
  mounted() {
    this.getTheater(this.theaterId);
    this.getMovies(this.theaterId);
  },
  methods: {
    goToMovie(id) {
      this.$router.push({ name: 'theater-movie', params: { theaterId: this.theaterId, movieId: id.toString() } });
    },
    getTheater(id) {
      TheController.retrieveTheater(id)
        .then((response) => {
          this.theater = new Theater(response.data);
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id) {
      TheaterController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
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
.cinema-list-item:hover {
  background: rgba(158, 158, 158, 0.4);
}
</style>
