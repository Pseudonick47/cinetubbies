<template>
  <div>
    <v-container>
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
      <v-layout
        class="theaters-container"
        row
      >
        <v-flex
          v-for="entry in entries"
          :key="entry.id"
          xs12
          sm6
          md4
          lg4
          xl4
          pa-3
        >
          <theater
            v-if="kind === 'theaters'"
            :info="entry"
            @editTheater="editTheater"
            @removeTheater="removeTheater"
          />
          <admin
            v-else
            :info="entry"
            @editAdmin="editTheater"
            @removeAdmin="removeTheater"
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
    <theater-dialog
      v-if="dialog && kind === 'theaters'"
      @close="dialog = false"
    />
    <admin-dialog
      v-else-if="dialog && kind === 'theater-admins'"
      kind="theater-admins"
      role="cinema_admin"
      @close="dialog = false"
    />
    <admin-dialog
      v-else-if="dialog && kind === 'fan-zone-admins'"
      kind="fan-zone-admins"
      role="fan_zone_admin"
      @close="dialog = false"
    />
  </div>
</template>

<script>
import * as _ from 'lodash';
import { mapGetters } from 'vuex';

import Admin from 'Components/SystemAdmin/Admin.component';
import AdminDialog from 'Components/SystemAdmin/AdminDialog.component';
import Theater from 'Components/SystemAdmin/Theater.component';
import TheaterDialog from 'Components/SystemAdmin/TheaterDialog.component';

import SystemAdminContorller from 'Controllers/system-admin.controller';

export default {
  name: 'SystemAdminHome',
  components: {
    Admin,
    AdminDialog,
    Theater,
    TheaterDialog
  },
  data() {
    return {
      dialog: false,
      gradient: 'to top, #1565C0, #42A5F5'
    };
  },
  computed: {
    ...mapGetters('systemAdmin', {
      entries: 'data',
      count: 'count'
    }),
    kind() {
      return this.$route.params.kind;
    },
    entriesPerPage: {
      get() {
        return this.$store.getters['systemAdmin/entriesPerPage'];
      },
      set(val) {
        SystemAdminContorller.setEntriesPerPage(val);
      }
    },
    page: {
      get() {
        return this.$store.getters['systemAdmin/page'];
      },
      set(val) {
        SystemAdminContorller.requestPage(val, this.kind);
        this.$store.commit('systemAdmin/setPage', val);
      }
    },
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    },
    theaterGrid() {
      return _.chunk(this.data, 4);
    }
  },
  watch: {
    $route(to, from) {
      SystemAdminContorller.requestCount(this.$route.params.kind);
      SystemAdminContorller.requestPage(1, this.$route.params.kind);
    }
  },
  beforeMount() {
    SystemAdminContorller.requestTheaterAdmins();
    SystemAdminContorller.requestCount(this.$route.params.kind);
    SystemAdminContorller.requestPage(1, this.$route.params.kind);
  },
  methods: {
    editTheater(id) {
      console.log('Edit theater', id);
    },

    removeTheater(id) {
      console.log('Remove theater', id);
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

.register-errors {
  color: red;
}
</style>
