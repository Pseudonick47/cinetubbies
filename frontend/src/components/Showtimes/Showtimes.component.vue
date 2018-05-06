<template>
  <v-layout row>
    <v-dialog
      v-model="dialog"
      max-width="700px">
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
                  v-model="showtime.auditorium"
                  :error-messages="errors.collect('auditorium')"
                  :counter="255"
                  label="Auditorium"
                  data-vv-name="auditorium"
                  required
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-validate="'required'"
                  v-model.number="showtime.price"
                  :error-messages="errors.collect('price')"
                  label="Price"
                  data-vv-name="price"
                  required
                />
              </v-flex>
              <v-layout row>
                <v-flex>
                  <v-date-picker
                    v-model="showtime.date"
                  />
                </v-flex>
                <v-flex>
                  <v-time-picker
                    v-model="time"
                  />
                </v-flex>
              </v-layout>
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
      md4
      offset-lg
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
          :headers="[{ text: kind, sortable: false, value: 'title' },]"
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ props.item.title }}</td>
            <td class="right layout px-0">
              <v-tooltip left>
                <v-btn
                  slot="activator"
                  icon
                  @click="create(props.item)">
                  <v-icon>add</v-icon>
                </v-btn>
                <span>New showtime</span>
              </v-tooltip>
              <v-tooltip right>
                <v-btn
                  slot="activator"
                  icon
                  @click="filter(props.item.id)">
                  <v-icon>list</v-icon>
                </v-btn>
                <span>See showtimes<br>for this movie</span>
              </v-tooltip>
            </td>
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
    <v-flex
      s12
      sm5
      md7
      offset-lg1>
      <v-card>
        <v-card-title>
          Showtimes
          <v-spacer/>
          <v-btn
            v-show="filtered"
            @click="removeFilter"
          >remove filter</v-btn>
        </v-card-title>
        <v-data-table
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
            <td>{{ props.item.date }}</td>
            <td>{{ props.item.time }}</td>
            <td>{{ props.item.price }}</td>
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
                  Delete this showtime?
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="remove(props.item.id)">yes</v-btn>
                  <v-spacer/>
                  <v-btn @click="confirmDelete = false">no</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
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
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import SysAdminController from 'Controllers/system-admin.controller';
import TheaterController from 'Controllers/theaters.controller';
import ShowtimeController from 'Controllers/showtimes.controller';
import { Movie } from 'Models/movie.model';
import { Showtime } from 'Models/showtime.model';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    search: '',
    movies: [],
    confirmDelete: false,
    showtimeToDelete: 0,
    theaterId: 0,
    showtime: new Showtime(),
    time: null,
    repertoire: [],
    kind: '',
    dialog: false,
    editedIndex: -1,
    filtered: false
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'headers'
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
      this.showtime = new Showtime();
      this.time = null;
      this.showtime.movie = movie.id;
      this.editedIndex = -1;
    },
    save() {
      this.dialog = false;
      this.showtime.time = this.time;
      if (this.editedIndex === -1) {
        ShowtimeController.create(this.showtime)
          .then((response) => {
            this.$alert.success('Successfully added!');
            this.getRepertoire();
          })
          .catch((response) => {
            this.$alert.error('Error occurred.');
          });
      } else {
        let data = _.reduce(this.showtime, (result, value, key) => {
          if (!_.isEmpty(value) || (key === 'price' && value !== null)) {
            result[key] = value;
          }
          return result;
        }, {});
        ShowtimeController.update(data, this.showtime.id).then((response) => {
          this.showtime = new Showtime(response.data);
          this.$alert.success('Settings successfully saved');
          this.getRepertoire();
        }).catch(() => {
          this.$alert.error('Error while saving settings');
        });
      }
    },
    getTheaterAndMovies() {
      SysAdminController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theaterId = response.data.id;
          if (response.data.kind === 'm') {
            this.kind = 'Movie';
          } else {
            this.kind = 'Play';
          }
          this.getMovies();
          this.getRepertoire();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id = this.theaterId) {
      SysAdminController.getMovies(id)
        .then((response) => {
          this.movies = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    deleteButton(id) {
      this.confirmDelete = true;
      this.showtimeToDelete = id;
    },
    remove() {
      this.confirmDelete = false;
      ShowtimeController.destroy(this.showtimeToDelete)
        .then((response) => {
          this.$alert.success('Successfully deleted!');
          this.getRepertoire();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    editButton(showtimeData) {
      this.showtime = new Showtime(showtimeData);
      this.time = this.showtime.time;
      this.editedIndex = 1;
      this.dialog = true;
    },
    getRepertoire() {
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
    },
    filter(id) {
      TheaterController.getRepertoire(this.theaterId)
        .then((response) => {
          this.filtered = true;
          this.repertoire = response.data.filter(s => s['movie'] === id);
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    removeFilter() {
      this.getRepertoire();
      this.filtered = false;
    }
  }
};
</script>

