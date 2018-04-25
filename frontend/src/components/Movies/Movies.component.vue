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
        <v-text-field
          v-validate="'required'"
          v-model="movie.title"
          :error-messages="errors.collect('title')"
          :counter="255"
          label="Title"
          data-vv-name="title"
          required
        />
        <v-text-field
          v-validate="'required'"
          :counter="255"
          v-model="movie.genre"
          :error-messages="errors.collect('genre')"
          label="Genre"
          data-vv-name="genre"
          required
        />
        <v-text-field
          :counter="255"
          v-model="movie.director"
          label="Director"
        />
        <v-text-field
          :counter="255"
          v-model="movie.actors"
          label="Actors"
        />
        <v-text-field
          :counter="255"
          v-model="movie.duration"
          label="Duration"
        />
        <v-text-field
          :counter="255"
          v-model="movie.description"
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
          :key="movie.id" >
          <v-list-tile-content>
            <v-list-tile-title>{{ movie.title }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ movie.genre }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action >
            <v-btn
              icon
              ripple
              @click.stop="confirmDelete = true"
            >
              <v-icon color="grey lighten-1">delete</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-dialog
            v-model="confirmDelete"
            persistent
            max-width="300px"
          >
            <v-card>
              <v-card-text>
                Delete this movie?
              </v-card-text>
            </v-card>
            <v-card-actions>
              <v-btn @click="remove(movie.id)">yes</v-btn>
              <v-spacer/>
              <v-btn @click="confirmDelete = false">no</v-btn>
            </v-card-actions>
          </v-dialog>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>

</template>

<script>
import MoviesController from 'Controllers/movies.controller';
import { Movie } from 'Models/movie.model';

export default {
  data: () => ({
    valid: true,
    loading: false,
    search: '',
    movies: [],
    movie: new Movie(),
    confirmDelete: false
  }),
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
    this.getMovies();
  },
  methods: {
    submit() {
      MoviesController.create(this.movie
      ).then((response) => {
        this.clear();
        this.getMovies();
        this.$alert.success('Successfully added!');
      }).catch((response) => {
        this.$alert.error('Error while saving.');
      });
    },
    clear() {
      this.movie = new Movie();
    },
    getMovies() {
      this.loading = true;
      MoviesController.getMovies()
        .then((response) => {
          this.movies = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    remove(id) {
      this.loading = true;
      this.confirmDelete = false;
      MoviesController.destroy(id)
        .then((response) => {
          this.loading = false;
          this.getMovies();
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
