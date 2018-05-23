<template>
  <div
    style="height: 100%; width: 100%"
  >
    <v-layout
      row
      justify-space-between
      my-5
      px-4
      style="height: auto"
    >
      <v-flex
        xs12
        sm12
        md4
      >
        <v-chip
          color="white"
          text-color="black">
          <v-icon left>build</v-icon>
          Theater settings
        </v-chip>
        <v-chip
          color="white"
          text-color="black">
          <span v-if="theater.isCinema()">Type: cinema</span>
          <span v-else>Type: theater</span>
          <v-tooltip right>
            <v-icon
              slot="activator"
              right
            >info</v-icon>
            <span>Types: cinema, theater</span>
          </v-tooltip>
        </v-chip>
        <v-card>
          <v-card-media
            v-if="theater.image"
            :src="theater.image.path"
            height="200px"
          />
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout
      column
      style="height: auto"
      mb-5
      px-4
    >
      <v-flex
        mt-2
        xs-12
        offset-lg1
      >
        <v-card>
          <v-card-title>
            Theater repertoire
            <v-spacer/>
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
            </template>
            <template slot="no-data">
              Sorry, nothing to display here.
            </template>
          </v-data-table>
        </v-card>
      </v-flex>
      <v-flex
        mt-4
        xs-12
        offset-lg1
      >
        <v-card>
          <v-card-title>
            Tickets on sale
            <v-spacer/>
          </v-card-title>
          <v-data-table
            :items="tickets"
            :headers="ticketsHeaders"
            item-key="date"
            class="elevation-1"
          >
            <template
              slot="items"
              slot-scope="props">
              <td>{{ getObjAttr(movies, getObjAttr(repertoire, props.item.showtime, 'movie'), 'title') }}</td>
              <td>{{ findObjectById(auditoriums, getObjAttr(repertoire, props.item.showtime, 'auditorium')).name }} </td>
              <td>{{ props.item.seat }} </td>
              <td>{{ getObjAttr(repertoire, props.item.showtime, 'date') }}</td>
              <td>{{ getObjAttr(repertoire, props.item.showtime,'time') }}</td>
              <td>{{ getObjAttr(repertoire, props.item.showtime,'price') }}</td>
              <td>{{ props.item.discount }}</td>
            </template>
            <template slot="no-data">
              Sorry, nothing to display here.
            </template>
          </v-data-table>
        </v-card>
      </v-flex>
      <v-flex
        mt-4
        xs-12
        offset-lg1
      >
        <v-card>
          <v-card-title>
            Auditoriums
            <v-spacer/>
            <v-btn
              icon
              @click="openAddAuditoriumDialog"
            >
              <v-icon color="accent">add_circle_outline</v-icon>
            </v-btn>
          </v-card-title>
          <v-data-table
            :items="auditoriums"
            hide-headers
            item-key="date"
            class="elevation-1"
          >
            <template
              slot="items"
              slot-scope="props">
              <td>
                <v-layout row>
                  <v-flex
                    md10
                    mt-3>
                    <p>{{ props.item.name }}</p>
                  </v-flex>
                  <v-flex
                    md2
                    xs2
                    lg2>
                    <v-btn
                      icon
                      @click="editAuditorium(props.item.id)">
                      <v-icon color="accent">edit</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      @click="deleteAuditorium(props.item.id)">
                      <v-icon color="accent">delete</v-icon>
                    </v-btn>
                  </v-flex>
                </v-layout>
              </td>
            </template>
            <template slot="no-data">
              Sorry, nothing to display here.
            </template>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
    <auditorium-dialog
      v-if="showAddAuditoriumModal"
      :show="showAddAuditoriumModal"
      :auditorium="selectedAuditorium"
      @auditorium-finished="addOrUpdateAuditorium"
      @cancel="closeAuditoriumModal"
    />
  </div>
</template>

<script>
import SysAdminController from 'Controllers/system-admin.controller';
import TheatersController from 'Controllers/theaters.controller';
import AuditoriumDialog from 'Components/Auditorium/AuditoriumDialog.component';
import { mapGetters } from 'vuex';
import { Theater } from 'Models/theater.model';
import { Showtime } from 'Models/showtime.model';
import { TicketOnSale } from 'Models/ticket-on-sale.model';
import { Movie } from 'Models/movie.model';
import MediaService from 'Api/media-upload.service';

export default {
  name: 'TheaterSettings',
  components: {
    AuditoriumDialog
  },
  data: () => ({
    loading: false,
    confirmSubmit: false,
    theater: new Theater(),
    repertoire: [],
    tickets: [],
    movies: [],
    selectedImage: null,
    auditoriums: [],
    auditoriumHeaders: [ { text: 'Name' } ],
    showAddAuditoriumModal: false,
    selectedAuditorium: null
  }),
  computed: {
    ...mapGetters([ 'activeUser', 'headers', 'ticketsHeaders' ])
  },
  mounted() {
    this.loadTheater();
  },
  methods: {
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
    },
    loadAuditoriums() {
      TheatersController.getAuditoriums(this.theater.id)
        .then((response) => {
          this.auditoriums = TheatersController.mapAuditoriums(response.data);
        })
        .catch((response) => {

        });
    },
    loadTheater() {
      this.loading = true;
      SysAdminController.getTheater(this.activeUser.id)
        .then(response => {
          this.theater = new Theater(response.data);
          this.loadAuditoriums();
          SysAdminController.getMovies(this.theater.id)
            .then(response => {
              this.movies = _.map(response.data, x => new Movie(x));
            })
            .catch(response => {
              this.$alert.error('Error occurred.');
            });
          TheatersController.getRepertoire(this.theater.id)
            .then(response => {
              this.repertoire = _.map(response.data, x => new Showtime(x));
            })
            .catch(response => {
              this.$alert.error('Error occurred.');
            });
          TheatersController.getTicketsOnSale(this.theater.id)
            .then(response => {
              this.tickets = _.map(response.data, x => new TicketOnSale(x));
            })
            .catch(response => {
              this.$alert.error('Error occurred.');
            });
          this.loading = false;
        })
        .catch(response => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    controllerUpdate(data) {
      SysAdminController.update(data, this.theater.id)
        .then(response => {
          this.$alert.success('Successfully saved');
        })
        .catch(() => {
          this.$alert.error('Error while saving settings');
        });
    },
    submit() {
      this.confirmSubmit = false;
      let data = _.reduce(
        this.theater,
        (result, value, key) => {
          if (!_.isEmpty(value)) {
            result[key] = value;
          }
          return result;
        },
        {}
      );
      this.$validator.validateAll().then(result => {
        if (result) {
          if (this.selectedImage === null) {
            this.controllerUpdate(data);
          } else {
            const fd = new FormData();
            fd.append('kind', 't');
            fd.append('data', this.selectedImage, this.selectedImage.name);
            MediaService.postImage(fd)
              .then(response => {
                data['image_id'] = response.data.id;
                this.controllerUpdate(data);
              })
              .catch(() => {
                this.$alert.error('Error while saving settings');
              });
          }
        }
      });
    },
    findObjectById(array, id) {
      let index = _.findIndex(array, o => {
        return o.id === id;
      });
      return array[index];
    },
    findObjectByKey(array, key, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
          return array[i];
        }
      }
      return null;
    },
    getObjAttr(array, id, attr) {
      var obj = this.findObjectByKey(array, 'id', id);
      if (obj !== null) {
        return obj[attr];
      }
    },
    editAuditorium(auditoriumId) {
      let index = _.findIndex(this.auditoriums, o => {
        return o.id === auditoriumId;
      });
      this.selectedAuditorium = _.cloneDeep(this.auditoriums[index]);
      this.showAddAuditoriumModal = true;
    },
    openAddAuditoriumDialog() {
      this.selectedAuditorium = null;
      this.showAddAuditoriumModal = true;
    },
    addOrUpdateAuditorium(auditorium) {
      // null or undefined !
      if (auditorium.id != null) {
        TheatersController.updateAuditorium(this.theater.id, auditorium)
          .then((response) => {
            this.$alert.success('Successfully updated auditorium');
            this.insertOrUpdateAuditorium(response.data);
            this.closeAuditoriumModal();
          })
          .catch(() => {
            this.$alert.error('Error while updated auditorium');
          });
        this.selectedAuditorium = null;
        return;
      }
      TheatersController.createAuditorium(this.theater.id, auditorium)
        .then((response) => {
          this.insertOrUpdateAuditorium(response.data);
          this.$alert.success('Successfully created auditorium');
          this.closeAuditoriumModal();
        })
        .catch(() => {
          this.$alert.error('Error while created auditorium');
        });
    },
    closeAuditoriumModal() {
      this.showAddAuditoriumModal = false;
      this.selectedAuditorium = null;
    },
    deleteAuditorium(id) {
      TheatersController.deleteAuditorium(this.theater.id, id)
        .then((response) => {
          this.removeAuditorium(id);
          this.$alert.success('Successfully deleted auditorium');
        })
        .catch(() => {
          this.$alert.error('Error while deleting auditorium');
        });
    },
    removeAuditorium(id) {
      let index = _.findIndex(this.auditoriums, { id });
      if (index > -1) {
        this.auditoriums.splice(index, 1);
      }
    },
    insertOrUpdateAuditorium(data) {
      let index = _.findIndex(this.auditoriums, { id: data.id });
      if (index < 0) {
        return this.auditoriums.push(data);
      }
      this.auditoriums.splice(index, 1, TheatersController.mapAuditoriums([ data ])[0]);
    }
  }
};
</script>
