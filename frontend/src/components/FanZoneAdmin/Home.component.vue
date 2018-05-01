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
          <official-prop
            :info="entry"
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
    <official-prop-dialog
      v-if="dialog"
      @close="dialog=false"
      @reload="reloadPage"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import OfficialProp from 'Components/FanZone/OfficialProp.component';
import OfficialPropDialog from 'Components/FanZoneAdmin/OfficialPropDialog.component';

import SystemAdminController from 'Controllers/system-admin.controller';
import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/official-props.controller';

export default {
  name: 'FanZoneAdminHome',
  components: {
    OfficialProp,
    OfficialPropDialog
  },
  data() {
    return {
      dialog: false,
      entriesPerPage: 9,
      page: 1
    };
  },
  computed: {
    ...mapGetters('props/official/', {
      entries: 'all',
      count: 'count'
    }),
    ...mapGetters({
      admin: 'activeUser'
    }),
    pageCount() {
      console.log(this.admin.theater);
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    },
    theater() {
      return this.admin.theater.id;
    }
  },
  watch: {
    page() {
      reloadPage();
    }
  },
  beforeMount() {
    SystemAdminController.requestAdminsTheater(this.$store.getters.activeUser.id)
      .then(() => {
        const theater = this.theater;
        CategoriesController.requestCategories();
        PropsController.requestCount({ theater });
        PropsController.requestPage(this.page, { theater });
      });
  },
  methods: {
    reloadPage() {
      PropsController.requestPage(this.page, { theater: this.theater });
    }
  }
};
</script>
<style>
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
