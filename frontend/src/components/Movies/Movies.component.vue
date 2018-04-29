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
          :key="movie.id" >
          <v-list-tile-content>
            <v-list-tile-title>{{ movie.title }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ movie.genre }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action >
            <v-btn
              icon
              ripple
              @click="editButton(movie.id)"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-action>
            <v-btn
              icon
              ripple
              @click.stop="deleteButton(movie.id)"
            >
              <v-icon>delete</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-dialog
            v-model="editDialog"
            max-width="500px"
            persistent>
            <v-card>
              <v-card-title>
                Change information
              </v-card-title>
              <v-card-text>
                <v-form
                  v-model="valid"
                >
                  <v-text-field
                    v-validate="'required'"
                    v-model="editingMovie.title"
                    :error-messages="errors.collect('title')"
                    :counter="255"
                    label="Title"
                    data-vv-name="title"
                    required
                  />
                  <v-text-field
                    :counter="255"
                    v-model="editingMovie.genre"
                    :error-messages="errors.collect('genre')"
                    label="Genre"
                    data-vv-name="genre"
                    required
                  />
                  <v-text-field
                    :counter="255"
                    v-model="editingMovie.director"
                    label="Director"
                  />
                  <v-text-field
                    :counter="255"
                    v-model="editingMovie.actors"
                    label="Actors"
                  />
                  <v-text-field
                    :counter="255"
                    v-model="editingMovie.duration"
                    label="Duration"
                  />
                  <v-text-field
                    :counter="255"
                    v-model="editingMovie.description"
                    label="Description"
                  />
                  <v-btn
                    :disabled="!valid"
                    @click="edit"
                  >
                    save
                  </v-btn>
                  <v-btn @click="editDialog=false">close</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-dialog>
          <!--<change-info-dialog
            valid="valid"
            movie="movie"
            editdialog="editDialog"/>-->
          <v-dialog
            v-model="confirmDelete"
            persistent
            max-width="300px"
          >
            <v-card>
              <v-card-text>
                Delete this movie?
              </v-card-text>
              <v-card-actions>
                <v-btn @click="remove(movie.id)">yes</v-btn>
                <v-spacer/>
                <v-btn @click="confirmDelete = false">no</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-list-tile>
      </v-list>
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
    valid: true,
    loading: false,
    search: '',
    movies: [],
    movie: new Movie(),
    confirmDelete: false,
    editDialog: false,
    editingMovie: new Movie(),
    deletingMovie: 0,
    theaterId: 0
  }),
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
      'activeUser'
    ])
  },
  mounted() {
    this.getTheaterAndMovies();
  },
  methods: {
    submit() {
      this.movie.theater = this.theaterId;
      MoviesController.create(this.movie
      ).then((response) => {
        this.clear();
        this.getMovies();
        this.$alert.success('Successfully added!');
      }).catch((response) => {
        this.$alert.error('Error while saving.');
      });
    },
    editButton(movieId) {
      MoviesController.retrieve(movieId).then((response) => {
        this.editingMovie = new Movie(response.data);
      }).catch(() => {
        this.$alert.error('Error occurred!');
      });
      this.editDialog = true;
    },
    deleteButton(id) {
      this.confirmDelete = true;
      this.deletingMovie = id;
    },
    edit() {
      let data = _.reduce(this.editingMovie, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      MoviesController.update(data, this.editingMovie.id).then((response) => {
        this.editDialog = false;
        this.editingMovie = new Movie(response.data);
        this.$alert.success('Settings successfully saved');
      }).catch(() => {
        this.$alert.error('Error while saving settings');
      });
    },
    clear() {
      this.movie = new Movie();
    },
    getTheaterAndMovies() {
      this.loading = true;
      TheaterController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theaterId = response.data.id;
          this.getMovies();
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id = this.theaterId) {
      this.loading = true;
      TheaterController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    remove() {
      this.loading = true;
      this.confirmDelete = false;
      MoviesController.destroy(this.deletingMovie)
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
