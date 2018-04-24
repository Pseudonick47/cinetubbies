<template>
  <div>
    <v-container>
      <v-layout
        row
        pa-2
      >
        <v-jumbotron
          :gradient="gradient"
          dark
        >
          <v-container
            fill-height
            pa-4
          >
            <v-layout align-center>
              <v-flex>
                <h3 class="display-3">Theaters</h3>
                <span class="subheading">Lorem ipsum dolor sit amet, pri veniam forensibus id. Vis maluisset molestiae id, ad semper lobortis cum. At impetus detraxit incorrupte usu, repudiare assueverit ex eum, ne nam essent vocent admodum.</span>
                <v-divider
                  color="white"
                  class="my-3"
                />
              </v-flex>
            </v-layout>
          </v-container>
        </v-jumbotron>
      </v-layout>
      <v-layout
        row
        pa-2
      >
        <v-card class="theaters-toolbar">
          <v-layout
            row
            pa-2
            justify-space-between
          >
            <v-text-field
              prepend-icon="search"
              label="Search"
              solo-inverted
              class="mx-3"
              flat
            />
            <v-btn
              color="primary"
              @click.native.stop="dialog=true"
            >New</v-btn>
          </v-layout>
        </v-card>
      </v-layout>
      <!-- <v-layout
        v-for="(row, i) in theaterGrid"
        :key="i"
        row
      > -->
      <v-layout
        class="theaters-container"
        row
      >
        <v-flex
          v-for="theater in theaters"
          :key="theater.id"
          xs12
          sm6
          md4
          lg4
          xl4
          pa-3
        >
          <theater
            :info="theater"
            class="theater-placeholder"
            @editTheater="editTheater"
            @removeTheater="removeTheater"
          />
        </v-flex>
      </v-layout>
    </v-container>
    <v-container id="pagination">
      <v-layout justify-center>
        <v-pagination
          :length="pageCount"
          :total-visible="7"
          v-model="page"
        />
      </v-layout>
    </v-container>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="500px"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Register new theater/cinema</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex
                xs12
                sm12
                md12
              >
                <v-text-field
                  v-model="new_theater_name"
                  label="Name"
                  required
                />
              </v-flex>
              <v-flex
                xs12
                sm12
                md12
              >
                <v-text-field
                  v-model="new_theater_address"
                  label="Address"
                />
              </v-flex>
              <v-flex
                xs12
                sm6
              >
                <v-select
                  v-model="new_theater_kind"
                  :items="['Cinema', 'Theater']"
                  label="Kind"
                  required
                />
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue darken-1"
            flat
            @click.native="resetDialog"
          >Close</v-btn>
          <v-btn
            color="blue darken-1"
            flat
            @click.native="registerNewTheater"
          >Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import * as _ from 'lodash';
import { mapGetters } from 'vuex';
import TheatersContorller from 'Controllers/theaters.controller';

import Theater from 'Components/Admin/Theater.component';

const MAP_KIND = {
  'Cinema': 'm',
  'Theater': 'p'
};

export default {
  name: 'AdminTheaters',
  components: {
    Theater
  },
  data() {
    return {
      dialog: false,
      new_theater_name: '',
      new_theater_address: '',
      new_theater_kind: 'Cinema',
      show: false,
      gradient: 'to top, #1565C0, #42A5F5'
    };
  },
  computed: {
    ...mapGetters([
      'theaters',
      'theatersCount'
    ]),
    entriesPerPage: {
      get() {
        return this.$store.getters.entriesPerPage;
      },
      set(val) {
        TheatersContorller.setEntriesPerPage(val);
      }
    },
    page: {
      get() {
        return this.$store.getters.page;
      },
      set(val) {
        TheatersContorller.requestPage(val);
        this.$store.commit('setPage', val);
      }
    },
    pageCount() {
      return _.ceil(_.divide(this.theatersCount + 1, this.entriesPerPage));
    },
    theaterGrid() {
      return _.chunk(this.theaters, 4);
    }
  },
  beforeMount() {
    TheatersContorller.requestTheaterCount();
    TheatersContorller.requestPage(1);
  },
  methods: {
    editTheater(id) {
      console.log('Edit theater', id);
    },
    removeTheater(id) {
      console.log('Remove theater', id);
    },
    resetDialog() {
      this.new_theater_name = '';
      this.new_theater_address = '';
      this.new_theater_kind = 'Cinema';

      this.dialog = false;
    },

    registerNewTheater() {
      // TODO: select real admin
      const newTheater = {
        name: this.new_theater_name,
        address: this.new_theater_address,
        admin_id: 2,
        kind: MAP_KIND[this.new_theater_kind]
      };
      TheatersContorller.registerNewTheater(newTheater);
      this.resetDialog();
    }
  }
};
</script>

<style>
#pagination {
  max-width: none;
}
.theaters-toolbar {
  width: 100%;
}
.theaters-container {
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;

  flex-flow: row wrap;
  -webkit-flex-flow: row wrap;
  justify-content: flex-start;
  align-items: stretch;
}
</style>
