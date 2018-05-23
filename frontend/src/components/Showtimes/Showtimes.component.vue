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
                <v-select
                  v-validate="'required'"
                  :items="auditoriums"
                  :error-messages="errors.collect('auditorium')"
                  v-model="showtime.auditorium"
                  item-text="name"
                  item-value="id"
                  data-vv-name="auditorium"
                  label="Select Auditorium"
                  single-line
                  requeired
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
                  suffix="$"
                  required
                  box
                  type="number"
                />
              </v-flex>
              <v-layout row>
                <v-flex>
                  <v-menu
                    :close-on-content-click="false"
                    v-model="dateMenu"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="290px"
                    min-width="290px"
                  >
                    <v-text-field
                      v-validate="'required'"
                      slot="activator"
                      v-model="showtime.date"
                      :error-messages="errors.collect('date')"
                      label="Date"
                      hint="YYYY-MM-DD format"
                      persistent-hint
                      prepend-icon="event"
                      readonly
                      required
                      data-vv-name="date"
                    />
                    <v-date-picker
                      v-model="showtime.date"
                      :min="today"
                      no-title
                      @input="dateMenu = false"/>
                  </v-menu>
                </v-flex>
                <span>&emsp;</span>
                <v-flex>
                  <v-menu
                    :close-on-content-click="false"
                    v-model="timeMenu"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="290px"
                    min-width="290px"
                  >
                    <v-text-field
                      v-validate="'required'"
                      slot="activator"
                      v-model="time"
                      :error-messages="errors.collect('time')"
                      label="Time"
                      hint="HH:mm format"
                      persistent-hint
                      prepend-icon="watch"
                      readonly
                      required
                      data-vv-name="time"
                    />
                    <v-time-picker
                      v-model="time"
                      @input="timeMenu = false"/>
                  </v-menu>
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
            <td>{{ getObjAttr(movies, props.item.movie, 'title') }}</td>
            <td>{{ findObjectById(auditoriums, props.item.auditorium).name }} </td>
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
import { Showtime } from 'Models/showtime.model';
import { mapGetters } from 'vuex';

var moment = require('moment');

export default {
  name: 'Showtimes',
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
    filtered: false,
    auditoriums: [],
    dateMenu: false,
    timeMenu: false
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'headers'
    ]),
    formTitle() {
      return this.editedIndex === -1 ? 'New ' + this.kind : 'Edit ' + this.kind;
    },
    today() {
      return moment().format('YYYY-MM-DD');
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
      this.$validator.validateAll().then((result) => {
        if (result) {
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
            ShowtimeController.update(data, this.showtime.id)
              .then((response) => {
                this.showtime = new Showtime(response.data);
                this.$alert.success('Settings successfully saved');
                this.getRepertoire();
              }).catch(() => {
                this.$alert.error('Error while saving settings');
              });
          }
        } else {
          this.$alert.error('Please fill all required fields correctly.');
        }
      });
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
          TheaterController.getAuditoriums(this.theaterId)
            .then((response) => {
              this.auditoriums = TheaterController.mapAuditoriums(response.data);
            })
            .catch((response) => {
              this.$alert.error('Error occurred. Please reload the page');
            });
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
    findObjectByKey(array, key, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
          return array[i];
        }
      }
      return null;
    },
    findObjectById(array, id) {
      let index = _.findIndex(array, o => {
        return o.id === id;
      });
      return array[index];
    },
    getObjAttr(array, id, attr) {
      var obj = this.findObjectByKey(array, 'id', id);
      if (obj !== null) {
        return obj[attr];
      }
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

