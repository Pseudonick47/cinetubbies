<template>
  <div>
    <v-parallax
      src="http://arab-culture.info/wp-content/uploads/2018/02/1-68.jpg"
      height="400"
    >
      <v-layout
        column
        align-center
        justify-center>
        <h1 class="white--text title-text-shadow">{{ theater.name }}</h1>
        <h4 class="white--text title-text-shadow">{{ theater.rating }} ★</h4>
      </v-layout>
    </v-parallax>
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
.title-text-shadow {
    text-shadow: 2px 2px 3px #555;
}
</style>
