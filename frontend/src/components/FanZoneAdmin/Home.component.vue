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
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import OfficialProp from 'Components/FanZoneAdmin/OfficialProp.component';
import PropsController from 'Controllers/props.controller';

export default {
  name: 'FanZoneAdminHome',
  components: {
    OfficialProp
  },
  data() {
    return {
      dialog: false,
      entriesPerPage: 9,
      page: 1,
      theater: 2
    };
  },
  computed: {
    ...mapGetters('props/official/', {
      entries: 'all',
      count: 'count'
    }),
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    }
  },
  watch: {
    page() {
      PropsController.requestOfficialProps(this.theater, this.page);
    }
  },
  beforeMount() {
    PropsController.requestCategories();
    PropsController.requestOfficialPropCount(this.theater);
    PropsController.requestOfficialProps(this.theater, this.page);
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
