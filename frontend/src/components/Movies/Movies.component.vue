<template>
  <v-layout row>
    <v-flex
      xs12
      sm5
      md3
      offset-lg2
    >
      <v-form
        v-model="valid"
      >
        <v-title>
          New movie/play
        </v-title>
        <v-text-field
          v-model="title"
          :rules="titleRules"
          :counter="255"
          label="Title"
          required
        />
        <v-text-field
          :counter="255"
          :rules="genreRules"
          v-model="genre"
          label="Genre"
          required
        />
        <v-text-field
          :counter="255"
          v-model="director"
          label="Director"
        />
        <v-text-field
          :counter="255"
          v-model="actors"
          label="Actors"
        />
        <v-text-field
          :counter="255"
          v-model="duration"
          label="Duration"
        />
        <v-text-field
          :counter="255"
          v-model="description"
          label="Description"
        />
        <v-btn
          :disabled="!valid"
          @click="submit"
        >
          add
        </v-btn>
        <v-btn @click="clear">clear</v-btn>
      </v-form>
    </v-flex>
    <v-flex
      s12
      sm5
      md5
      offset-lg2
    >
      <v-list
        two-line
        subheader
      >
        <v-subheader>Movies</v-subheader>
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
          :key="movie.title" >
          <v-list-tile-content>
            <v-list-tile-title>{{ movie.title }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ movie.genre }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action >
            <v-btn
              icon
              ripple
              @click="remove(movie.id)"
            >
              <v-icon color="grey lighten-1">delete</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>

</template>

<script>
import MoviesController from 'Controllers/movies.controller';

export default {
  data: () => ({
    valid: true,
    loading: false,
    search: '',
    movies: [],
    title: '',
    genre: '',
    director: '',
    actors: '',
    duration: '',
    description: '',
    titleRules: [
      v => !!v || 'Title is required',
      v => (v && v.length <= 255) || 'Name must be less than 255 characters'
    ],
    genreRules: [
      v => !!v || 'Genre is required',
      v => (v && v.length <= 255) || 'Genre must be less than 255 characters'
    ]
  }),
  computed: {
    filteredMovies() {
      if (this.search !== '') {
        return this.movies.filter((i) => {
          return i.title.toLowerCase().includes(this.search.toLowerCase());
        });
      }
      return this.movies;
    }
  },
  mounted() {
    this.getMovies();
  },
  methods: {
    submit() {
      MoviesController.create({
        title: this.title,
        genre: this.genre,
        director: this.director,
        actors: this.actors,
        duration: this.duration,
        description: this.description
      }).then((response) => {
        this.clear();
        this.getMovies();
        this.$alert.success('Successfully added!');
      }).catch((response) => {
        this.$alert.error('Error while saving.');
      });
    },
    clear() {
      this.title = '';
      this.genre = '';
      this.director = '';
      this.actors = '';
      this.duration = '';
      this.description = '';
    },
    getMovies() {
      this.loading = true;
      MoviesController.getMovies()
        .then((response) => {
          this.movies = response.data;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    remove(id) {
      this.loading = true;
      MoviesController.destroy(id)
        .then((response) => {
          this.loading = false;
          this.getMovies();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    }
  }
};
</script>
