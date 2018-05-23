<template>
  <v-layout column>
    <v-dialog
      v-model="dialog"
      max-width="500px">
      <v-btn
        slot="activator"
        color="primary"
        dark
        class="mb-2"
        @click="create">New {{ kind }}</v-btn>
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
                  :width="20"
                  label="Title"
                  data-vv-name="title"
                  required
                  box
                />
                <span>&emsp;</span>
                <v-select
                  v-validate="'required'"
                  v-model="movie.genre"
                  :items="getGenres()"
                  :error-messages="errors.collect('genre')"
                  label="Genre"
                  data-vv-name="genre"
                  required
                  box
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  :counter="255"
                  :rows="2"
                  v-model="movie.description"
                  label="Description"
                  multi-line
                  box
                  auto-grow
                />
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-layout row>
                  <v-text-field
                    :counter="255"
                    v-model="newDirector"
                    label="Director"
                    box
                  />
                  <v-tooltip bottom>
                    <v-btn
                      slot="activator"
                      icon
                      @click="addNewDirector()">
                      <v-icon>add</v-icon>
                    </v-btn>
                    <span>Add director</span>
                  </v-tooltip>
                </v-layout>
                <v-flex>
                  <v-expansion-panel>
                    <v-expansion-panel-content>
                      <div slot="header">Directors</div>
                      <v-card
                        v-for="(item,i) in directors"
                        :key="i"
                      >
                        <v-layout row>
                          <v-card-text style="word-wrap: break-word;">{{ item }}</v-card-text>
                          <v-card-actions>
                            <v-btn
                              icon
                              @click="editDirector(i)">
                              <v-icon small>edit</v-icon>
                            </v-btn>
                            <v-btn
                              icon
                              @click="deleteDirector(i)">
                              <v-icon small>delete</v-icon
                            ></v-btn>
                          </v-card-actions>
                          <v-dialog
                            v-model="showEditDirDialog"
                            width="300px">
                            <v-card>
                              <v-card-text>Edit director</v-card-text>
                              <v-text-field
                                v-model="editingDirector.director"
                                label="Director"
                                box
                              />
                              <v-card-actions>
                                <v-btn @click="showEditDirDialog=false">close</v-btn>
                                <v-btn @click="saveEditedDirector()">save</v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
                        </v-layout>
                      </v-card>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-flex>
                <v-layout row>
                  <v-text-field
                    :counter="255"
                    v-model="newActor"
                    label="Actor"
                    box
                  />
                  <v-tooltip bottom>
                    <v-btn
                      slot="activator"
                      icon
                      @click="addNewActor()">
                      <v-icon>add</v-icon>
                    </v-btn>
                    <span>Add actor</span>
                  </v-tooltip>
                </v-layout>
              </v-flex>
              <v-flex>
                <v-expansion-panel>
                  <v-expansion-panel-content>
                    <div slot="header">Actors</div>
                    <v-card
                      v-for="(item,i) in actors"
                      :key="i"
                    >
                      <v-layout row>
                        <v-card-text style="word-wrap: break-word;">{{ item }}</v-card-text>
                        <v-card-actions>
                          <v-btn
                            icon
                            @click="editActor(i)">
                            <v-icon small>edit</v-icon>
                          </v-btn>
                          <v-btn
                            icon
                            @click="deleteActor(i)">
                            <v-icon small>delete</v-icon
                          ></v-btn>
                        </v-card-actions>
                        <v-dialog
                          v-model="showEditActDialog"
                          width="300px">
                          <v-card>
                            <v-card-text>Edit actor</v-card-text>
                            <v-text-field
                              v-model="editingActor.actor"
                              label="Actor"
                              box
                            />
                            <v-card-actions>
                              <v-btn @click="showEditActDialog=false">close</v-btn>
                              <v-btn @click="saveEditedActor(i)">save</v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </v-layout>
                    </v-card>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-model.number="movie.duration"
                  label="Duration"
                  box
                  suffix="min"
                />
                <v-chip
                  label
                  outline
                >
                  Poster image
                  <span>&emsp;</span>
                  <input
                    type="file"
                    @change="imageSelected"
                ></v-chip>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="
blue darken-1"
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
import MediaService from 'Api/media-upload.service';

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
    kind: '',
    selectedImage: null,
    newActor: '',
    actors: [],
    newDirector: '',
    directors: [],
    showEditDirDialog: false,
    showEditActDialog: false,
    editingDirector: { index: '', director: '' },
    editingActor: { index: '', actor: '' }
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'movieHeaders',
      'theaterGenres',
      'cinemaGenres'
    ]),
    formTitle() {
      return this.editedIndex === -1 ? 'New ' + this.kind : 'Edit ' + this.kind;
    }
  },
  mounted() {
    this.getTheaterAndMovies();
  },
  methods: {
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
    },
    create(movie) {
      this.dialog = true;
      this.movie = new Movie(movie);
      this.editedIndex = -1;
      this.actors = [];
      this.directors = [];
    },
    controllerCreate() {
      this.movie.actors = this.actors.join(',');
      this.movie.director = this.directors.join(',');
      this.actors = [];
      this.directors = [];
      MoviesController.create(this.movie)
        .then((response) => {
          this.$alert.success('Successfully saved');
          this.getMovies();
        })
        .catch((response) => {
          this.$alert.error('Error while saving.');
        });
    },
    controllerUpdate(data) {
      MoviesController.update(data, this.movie.id)
        .then((response) => {
          this.movie = new Movie(response.data);
          this.$alert.success('Settings successfully saved');
          this.getMovies();
        })
        .catch((response) => {
          this.$alert.error('Error while saving settings');
        });
    },
    save() {
      this.$validator.validateAll().then((result) => {
        if (result) {
          this.dialog = false;
          if (this.editedIndex === -1) {
            this.movie.theater = this.theaterId;
            if (this.selectedImage === null) {
              this.controllerCreate();
            } else {
              const fd = new FormData();
              fd.append('kind', 'm');
              fd.append('data', this.selectedImage, this.selectedImage.name);
              MediaService.postImage(fd)
                .then((response) => {
                  this.movie.image_id = response.data.id;
                  this.controllerCreate();
                }).catch(() => {
                  this.$alert.error('Error while saving settings');
                });
            }
          } else {
            let data = _.reduce(this.movie, (result, value, key) => {
              if (!_.isEmpty(value)) {
                result[key] = value;
              }
              return result;
            }, {});
            if (this.selectedImage === null) {
              this.controllerUpdate(data);
            } else {
              const fd = new FormData();
              fd.append('kind', 'm');
              fd.append('data', this.selectedImage, this.selectedImage.name);
              MediaService.postImage(fd)
                .then((response) => {
                  data['image_id'] = response.data.id;
                  this.controllerUpdate(data);
                }).catch(() => {
                  this.$alert.error('Error while saving settings');
                });
            }
          }
        } else {
          this.$alert.error('Please fill all required fields correctly.');
        }
      });
    },
    editButton(movieData) {
      this.movie = new Movie(movieData);
      this.editedIndex = 1;
      this.actors = this.movie.actors.split(',');
      this.directors = this.movie.director.split(',');
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
          this.$alert.error('Error occurred.  Tip:Movie cannot be deleted if there are showtimes for it.');
        });
    },
    addNewActor() {
      this.actors.push(this.newActor);
      this.newActor = '';
    },
    addNewDirector() {
      this.directors.push(this.newDirector);
      this.newDirector = '';
    },
    getGenres() {
      if (this.kind === 'm') {
        return this.cinemaGenres;
      } else {
        return this.theaterGenres;
      }
    },
    deleteDirector(i) {
      this.directors.splice(i, 1);
    },
    deleteActor(i) {
      this.actors.splice(i, 1);
    },
    editDirector(i) {
      this.showEditDirDialog = true;
      this.editingDirector.director = this.directors[i];
      this.editingDirector.index = i;
    },
    saveEditedDirector() {
      this.showEditDirDialog = false;
      this.directors[this.editingDirector.index] = this.editingDirector.director;
      this.movie.director = this.directors.join(',');
    },
    editActor(i) {
      this.showEditActDialog = true;
      this.editingActor.actor = this.actors[i];
      this.editingActor.index = i;
    },
    saveEditedActor() {
      this.showEditActDialog = false;
      this.actors[this.editingActor.index] = this.editingActor.actor;
      this.movie.actors = this.actors.join(',');
    }
  }
};
</script>
