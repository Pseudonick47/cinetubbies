<template>
  <div>
    <v-btn
      color="primary"
      @click.native.stop="dialog=true"
    >New</v-btn>
    <v-container>
      <v-layout
        v-for="theater in theaters"
        :key="theater.id"
        row
        my-3
      >
        <v-flex xs12>
          <v-card
            color="cyan darken-2"
            class="white--text"
          >
            <v-container
              fluid
              grid-list-lg
            >
              <v-layout row>
                <v-flex
                  xs7
                  pa-3
                >
                  <div>
                    <div class="headline mb-1">{{ theater.name }}</div>
                    <div>{{ theater.address }}</div>
                  </div>
                </v-flex>
                <v-flex xs5>
                  <v-card-media
                    src="http://arab-culture.info/wp-content/uploads/2018/02/1-68.jpg"
                    height="250px"
                    contain
                  />
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
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

const MAP_KIND = {
  'Cinema': 'm',
  'Theater': 'p'
};

export default {
  name: 'AdminTheaters',
  data() {
    return {
      dialog: false,
      new_theater_name: '',
      new_theater_address: '',
      new_theater_kind: 'Cinema'
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
    }
  },
  beforeMount() {
    TheatersContorller.requestTheaterCount();
    TheatersContorller.requestPage(1);
  },
  methods: {
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
/* .theater-container {
} */

#pagination {
  /* position: fixed;
  bottom: 5%; */
  max-width: none;
}
</style>
