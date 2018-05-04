<template>
  <v-layout row>
    <v-flex
      xs-12
      sm5
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
      <form>
        <v-text-field
          v-model="theater.name"
          label="Name"
        />
        <v-text-field
          v-model="theater.address"
          label="Address"
        />
        <v-text-field
          v-model="theater.description"
          label="Description"
        />
        <v-btn @click="confirmSubmit = true">submit</v-btn>
      </form>
      <v-dialog
        v-model="confirmSubmit"
        persistent
        max-width="300px"
      >
        <v-card>
          <v-card-text>
            Submit changes?
          </v-card-text>
          <v-card-actions>
            <v-btn @click="submit">yes</v-btn>
            <v-spacer/>
            <v-btn @click="confirmSubmit = false">no</v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>
    </v-flex>
    <v-flex
      xs-12
      offset-lg2
    >
      Theater repertoire:
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
    </v-flex>
  </v-layout>
</template>

<script>
import SysAdminController from 'Controllers/system-admin.controller';
import TheatersController from 'Controllers/theaters.controller';
import { mapGetters } from 'vuex';
import { Theater } from 'Models/theater.model';

export default {
  name: 'TheaterSettings',

  data: () => ({
    loading: false,
    confirmSubmit: false,
    theater: new Theater(),
    repertoire: [],
    movies: []
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'headers'
    ])
  },
  mounted() {
    this.loadTheater();
  },
  methods: {
    loadTheater() {
      this.loading = true;
      SysAdminController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theater = new Theater(response.data);
          SysAdminController.getMovies(this.theater.id)
            .then((response) => {
              this.movies = response.data;
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
          TheatersController.getRepertoire(this.theater.id)
            .then((response) => {
              this.repertoire = response.data;
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    submit() {
      this.confirmSubmit = false;
      let data = _.reduce(this.theater, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      this.$validator.validateAll().then((result) => {
        if (result) {
          SysAdminController.update(data, this.theater.id).then((response) => {
            this.$alert.success('Settings successfully saved');
          }).catch(() => {
            this.$alert.error('Error while saving settings');
          });
          return;
        }
        this.$alert.error('Error while saving settings');
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
