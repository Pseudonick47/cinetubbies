<template>
  <v-layout row>
    <v-flex
      s12
      sm5
      md5
      offset-lg
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
            <v-tooltip bottom>
              <v-btn
                slot="activator"
                icon
                ripple
                @click="createDialog(movie)"
              >
                <v-icon>
                  add</v-icon></v-btn>
              <span>New show time</span>
            </v-tooltip>
          </v-list-tile-action>
          <v-list-tile-action >
            <v-tooltip bottom>
              <v-btn
                slot="activator"
                icon
                ripple
                @click="show(movie.id, movie.name)"
              >
                <v-icon>
                  list</v-icon></v-btn>
              <span>See showtimes</span>
            </v-tooltip>
          </v-list-tile-action>
        </v-list-tile>
        <v-dialog
          v-model="createDialogBool"
          max-width="500px"
        >
          <v-card>
            <v-card-title>
              New showtime
            </v-card-title>
            <v-card-text>
              <v-form
                v-model="valid"
              >
                <v-text-field
                  v-validate="'required'"
                  v-model="showtime.auditorium"
                  :error-messages="errors.collect('auditorium')"
                  :counter="255"
                  label="Auditorium"
                  data-vv-name="auditorium"
                  required
                />
                <v-date-picker
                  v-model="showtime.date"
                />
                <v-time-picker
                  v-model="time"
                />
                <v-text-field
                  v-validate="'required'"
                  v-model.number="showtime.price"
                  :error-messages="errors.collect('price')"
                  label="Price"
                  data-vv-name="price"
                  required
                />
                <v-btn
                  :disabled="!valid"
                  @click="create"
                >
                  add
                </v-btn>
                <v-btn @click="clear">clear</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-list>
    </v-flex>
    <v-tooltip bottom>
      <v-btn
        slot="activator"
        @click="showRepertoire()">
        repertoire
      </v-btn>
      <span>See all showtimes</span>
    </v-tooltip>
    <v-flex
      s12
      sm5
      md5
      offset-lg1>
      <v-data-table
        v-show="showTable"
        :items="repertoire"
        :headers="headers"
        item-key="date"
        class="elevation-1"
      >
        <template
          slot="items"
          slot-scope="props">
          <td>{{ `${movieTitle(props.item.movie).title}` }}</td>
          <td>{{ `${props.item.auditorium}` }} </td>
          <td class="text-xs-right">{{ props.item.date }}</td>
          <td class="text-xs-right">{{ props.item.time }}</td>
          <td class="text-xs-right">{{ props.item.price }}</td>
        </template>
        <template slot="no-data">
          <v-alert
            :value="true"
            color="error"
            icon="warning">
            Sorry, nothing to display here.
          </v-alert>
        </template>
      </v-data-table>
      <v-list
        v-show="showShowtimes"
        two-line
        subheader
      >
        <v-subheader>Showtimes</v-subheader>
        <v-list-tile
          v-for="show in showtimes"
          :key="show.id" >
          <v-list-tile-content>
            <v-list-tile-title>auditorium: {{ show.auditorium }}, price: {{ show.price }}din</v-list-tile-title>
            <v-list-tile-sub-title>{{ show.time }}, {{ show.date }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action >
            <v-btn
              icon
              ripple
              @click="editButton(show.id)"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-action>
            <v-btn
              icon
              ripple
              @click.stop="deleteButton(show.id)"
            >
              <v-icon>delete</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-dialog
            v-model="editDialog"
            max-width="500px"
          >
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
                    v-model="editingShowtime.auditorium"
                    :error-messages="errors.collect('auditorium')"
                    :counter="255"
                    label="Auditorium"
                    data-vv-name="auditorium"
                    required
                  />
                  <v-date-picker
                    v-model="editingShowtime.date"
                  />
                  <v-time-picker
                    v-model="editingShowtime.time"
                  />
                  <v-text-field
                    v-validate="'required'"
                    v-model="editingShowtime.price"
                    :error-messages="errors.collect('price')"
                    label="Price"
                    data-vv-name="price"
                    required
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
          <v-dialog
            v-model="confirmDelete"
            persistent
            max-width="300px"
          >
            <v-card>
              <v-card-text>
                Delete this showtime?
              </v-card-text>
              <v-card-actions>
                <v-btn @click="remove(show.id)">yes</v-btn>
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
import SysAdminController from 'Controllers/system-admin.controller';
import TheaterController from 'Controllers/theaters.controller';
import ShowtimeController from 'Controllers/showtimes.controller';
import MovieController from 'Controllers/movies.controller';
import { Movie } from 'Models/movie.model';
import { Showtime } from 'Models/showtime.model';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    valid: true,
    loading: false,
    search: '',
    movies: [],
    movie: new Movie(),
    confirmDelete: false,
    deletingShowtime: 0,
    editingShowtime: new Showtime(),
    theaterId: 0,
    createDialogBool: false,
    showtime: new Showtime(),
    modal: false,
    time: null,
    showtimes: [],
    showShowtimes: false,
    movieName: '',
    editDialog: false,
    showTable: false,
    repertoire: []
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
      'activeUser',
      'headers'
    ])
  },
  mounted() {
    this.getTheaterAndMovies();
  },
  methods: {
    createDialog(movie) {
      this.createDialogBool = true;
      this.showtime.movie = movie.id;
    },
    create() {
      this.showtime.time = this.time;
      this.createDialogBool = false;
      ShowtimeController.create(this.showtime)
        .then((response) => {
          this.$alert.success('Successfully added!');
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    opetDialog() {
      this.showDialog = true;
    },
    clear() {
      this.showtime = new Showtime();
    },
    getTheaterAndMovies() {
      this.loading = true;
      SysAdminController.getTheater(this.activeUser.id)
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
      SysAdminController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    show(movieId) {
      this.showTable = false;
      MovieController.getShowtimes(movieId)
        .then((response) => {
          this.showtimes = _.map(response.data, x => new Showtime(x));
          this.showShowtimes = true;
        })
        .catch((resposne) => {
          this.$alert.error('Error occurred.');
        });
    },
    deleteButton(id) {
      this.confirmDelete = true;
      this.deletingShowtime = id;
    },
    remove() {
      this.confirmDelete = false;
      ShowtimeController.destroy(this.deletingShowtime)
        .then((response) => {
          this.$alert.success('Successfully deleted!');
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    editButton(showId) {
      this.editingShowtime = this.showtimes.find((element) => {
        return element.id === showId;
      });
      this.editDialog = true;
    },
    edit() {
      let data = _.reduce(this.editingShowtime, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      ShowtimeController.update(data, this.editingShowtime.id).then((response) => {
        this.editDialog = false;
        this.editingShowtime = new Showtime(response.data);
        this.$alert.success('Settings successfully saved');
      }).catch(() => {
        this.$alert.error('Error while saving settings');
      });
    },
    showRepertoire() {
      this.showTable = true;
      this.showShowtimes = false;
      TheaterController.getRepertoire(this.theaterId)
        .then((response) => {
          this.repertoire = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    movieTitle(id) {
      return this.movies.find((element) => {
        return element.id === id;
      });
    }
  }
};
</script>

