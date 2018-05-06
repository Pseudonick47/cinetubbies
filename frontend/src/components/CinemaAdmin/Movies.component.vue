<template>
  <v-layout column>
    <v-dialog
      v-model="dialog"
      max-width="500px">
      <v-btn
        slot="activator"
        color="primary"
        dark
        class="mb-2">New {{ kind }}</v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout
              column>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-validate="'required'"
                  v-model="movie.title"
                  :error-messages="errors.collect('title')"
                  :counter="255"
                  label="Title"
                  data-vv-name="title"
                  required
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-validate="'required'"
                  :counter="255"
                  v-model="movie.genre"
                  :error-messages="errors.collect('genre')"
                  label="Genre"
                  data-vv-name="genre"
                  required
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  :counter="255"
                  v-model="movie.director"
                  label="Director"
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  :counter="255"
                  v-model="movie.actors"
                  label="Actors"
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  :counter="255"
                  v-model="movie.duration"
                  label="Duration"
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  :counter="255"
                  v-model="movie.description"
                  label="Description"
                />
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="blue darken-1"
            flat
            @click="dialog = false">Cancel</v-btn>
          <v-btn
            color="blue darken-1"
            flat
            @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-flex
    >
      <v-card>
        <v-card-title>
          {{ kind }}s
          <v-spacer/>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          />
        </v-card-title>
        <v-data-table
          :items="movies"
          :search="search"
          :headers="movieHeaders"
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ props.item.title }}</td>
            <td>{{ props.item.genre }}</td>
            <td>{{ props.item.director }}</td>
            <td>{{ props.item.actors }}</td>
            <td>{{ props.item.duration }}</td>
            <td>{{ props.item.description }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                slot="activator"
                icon
                @click="editButton(props.item)">
                <v-icon>edit</v-icon>
              </v-btn>
              <v-btn
                slot="activator"
                icon
                @click="deleteButton(props.item.id)">
                <v-icon>delete</v-icon>
              </v-btn>
            </td>
            <v-dialog
              v-model="confirmDelete"
              persistent
              max-width="300px"
            >
              <v-card>
                <v-card-text>
                  Delete this  {{ kind }} ?
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="remove">yes</v-btn>
                  <v-spacer/>
                  <v-btn @click="confirmDelete = false">no</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </template>
          <v-alert
            slot="no-results"
            :value="true"
            color="error"
            icon="warning">
            Your search for "{{ search }}" found no results.
          </v-alert>
          <template slot="no-data">
            Sorry, nothing to display here.
          </template>
        </v-data-table>
      </v-card>
    </v-flex>
  </v-layout>

</template>

<script>
import MoviesController from 'Controllers/movies.controller';
import TheaterController from 'Controllers/system-admin.controller';
import { Movie } from 'Models/movie.model';
import { mapGetters } from 'vuex';
import ChangeInfoDialog from './ChangeInfo.component';

export default {
  components: {
    'change-info-dialog': ChangeInfoDialog
  },
  data: () => ({
    search: '',
    movies: [],
    movie: new Movie(),
    confirmDelete: false,
    deletingMovie: 0,
    theaterId: 0,
    dialog: false,
    editedIndex: -1,
    kind: ''
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'movieHeaders'
    ]),
    formTitle() {
      return this.editedIndex === -1 ? 'New ' + this.kind : 'Edit ' + this.kind;
    }
  },
  mounted() {
    this.getTheaterAndMovies();
  },
  methods: {
    create(movie) {
      this.dialog = true;
      this.movie = new Movie(movie);
      this.editedIndex = -1;
    },
    save() {
      this.dialog = false;
      if (this.editedIndex === -1) {
        this.movie.theater = this.theaterId;
        MoviesController.create(this.movie
        ).then((response) => {
          this.$alert.success('Successfully added!');

          this.getMovies();
        }).catch((response) => {
          this.$alert.error('Error while saving.');
        });
      } else {
        let data = _.reduce(this.movie, (result, value, key) => {
          if (!_.isEmpty(value)) {
            result[key] = value;
          }
          return result;
        }, {});
        MoviesController.update(data, this.movie.id).then((response) => {
          this.movie = new Movie(response.data);
          this.$alert.success('Settings successfully saved');

          this.getMovies();
        }).catch(() => {
          this.$alert.error('Error while saving settings');
        });
      }
    },
    editButton(movieData) {
      this.movie = new Movie(movieData);
      this.editedIndex = 1;
      this.dialog = true;
    },
    deleteButton(id) {
      this.confirmDelete = true;
      this.deletingMovie = id;
    },
    getTheaterAndMovies() {
      TheaterController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theaterId = response.data.id;
          if (response.data.kind === 'm') {
            this.kind = 'Movie';
          } else {
            this.kind = 'Play';
          }
          this.getMovies();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id = this.theaterId) {
      TheaterController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    remove() {
      this.confirmDelete = false;
      MoviesController.destroy(this.deletingMovie)
        .then((response) => {
          this.getMovies();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
