<template>
  <v-container
    class="content-container"
    fluid
  >
    <v-layout
      class="content-container"
      row
    >
      <v-flex sm2>
        <v-navigation-drawer
          style="padding: 0 !important"
        >
          <h1 class="pa-3">Official Props</h1>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-content
              hide-actions
              ripple
            >
              <div
                slot="header"
                @click.stop="categorySelected(-1)"
              >
                Display All Props
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <categories
            :collection="rootCategories"
            @select="categorySelected"
          />
        </v-navigation-drawer>
      </v-flex>
      <v-flex>
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
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import OfficialProp from 'Components/FanZone/OfficialProp.component';
import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/official-props.controller';

import * as _ from 'lodash';

export default {
  name: 'FanZoneHome',
  components: {
    Categories,
    OfficialProp
  },
  data() {
    return {
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
    ...mapGetters('props/categories/', {
      rootCategories: 'roots',
      categoryPath: 'path'
    }),
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    }
  },
  watch: {
    page() {
      PropsController.requestPage(this.page);
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    PropsController.requestCount();
    PropsController.requestPage(this.page);
  },
  methods: {
    categorySelected(id) {
      if (id === -1) {
        PropsController.requestCount();
        PropsController.requestPage(this.page);
      } else {
        PropsController.requestCount({ category: id });
        PropsController.requestPage(this.page, { category: id });
      }
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

.categories-container {
  position: relative;
  left: 0;
  top: 0;
  display: flex;
  align-self: stretch;
}

.content-container {
  padding: 0;
  height: 100%;
}
</style>
