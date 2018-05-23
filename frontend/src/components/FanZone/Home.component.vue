<template>
  <div style="width: 100%; height: 100%">
    <v-navigation-drawer
      v-model="drawer"
      class="shop-drawer pl-2 pt-4"
      app
      right
    >
      <div class="px-3">
        <v-text-field
          v-model="searchTerm"
          name="input-1-3"
          label="Prop title"
          single-line
          prepend-icon="search"
          mb-0
        />
        <v-btn
          class="mb-3"
          small
          block
          @click="searchProps"
        >Search</v-btn>
        <v-switch
          v-model="showOfficialProps"
          class="title"
          label="Official props"
          color="primary"
        />
        <v-switch
          v-model="showUsedProps"
          class="title"
          label="Used props"
          color="primary"
        />
      </div>
      <div class="title pa-3">Categories</div>
      <v-expansion-panel
        class="elevation-0"
        color="black"
      >
        <v-expansion-panel-content
          hide-actions
          ripple
        >
          <div
            slot="header"
            @click.stop="categorySelected(-1)"
          >
            All Categories
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <categories
        :collection="rootCategories"
        style="background-color: black"
        @select="categorySelected"
      />
    </v-navigation-drawer>
    <v-container
      class="content-container"
      fluid
      pt-3
    >
      <v-layout
        class="content-container"
        row
      >
        <v-flex
          hidden-sm-and-down
          md1
        />
        <v-flex style="display: flex; flex-direction: column;">
          <div>
            <v-container style="align-items: stretch;">
              <v-layout class="props-row">
                <v-flex
                  v-for="(prop, i) in props"
                  :key="i"
                  class="prop-container"
                  xs12
                  sm6
                  md4
                  lg3
                  xl3
                  pa-3
                >
                  <prop
                    :prop="prop"
                    @click.native="goToProp(prop)"
                  />
                </v-flex>
              </v-layout>
            </v-container>
            <v-container
              id="pagination"
              style="display: flex; flex-direction: column; align-items: center;"
            >
              <v-layout>
                <v-pagination
                  :length="pageCount"
                  :total-visible="7"
                  v-model="page"
                  style=" align-self: flex-end;"
                />
              </v-layout>
            </v-container>
          </div>
        </v-flex>

        <v-flex
          hidden-sm-and-down
          md1
          style="display: flex; align-items: center; justify-content: flex-end"
        >
          <v-btn
            fab
            small
            color="black"
            style="transform: scale(0.8);"
            @click="drawer = !drawer"
          >
            <v-icon>keyboard_arrow_right</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <prop-detail
      v-if="propToDisplay"
      :prop="propToDisplay"
      @close="propToDisplay = null"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import Prop from 'Components/FanZone/Prop.component';
import PropDetail from 'Components/FanZone/PropDetail.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/props.controller';

import * as _ from 'lodash';

export default {
  name: 'FanZoneHome',
  components: {
    Categories,
    Prop,
    PropDetail
  },
  data() {
    return {
      drawer: false,
      propToDisplay: null,
      entriesPerPage: 9,
      page: 1,
      showOfficialProps: true,
      showUsedProps: false,
      searchTerm: null
    };
  },
  computed: {
    ...mapGetters('props/', {
      props: 'all',
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
    goToProp(prop) {
      this.$router.push({ name: 'fan-zone-prop', params: { id: prop.id } });
    },
    categorySelected(id) {
      if (id === -1) {
        PropsController.requestCount();
        PropsController.requestPage(this.page);
      } else {
        PropsController.requestCount({ category: id });
        PropsController.requestPage(this.page, { category: id });
      }
    },
    searchProps() {
      const terms = { title: this.searchTerm };

      PropsController.requestCount(terms);
      PropsController.requestPage(this.page, terms);

      this.searchTerm = null;
    }
  }
};
</script>
<style>
.props-container {
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;

  flex-direction: column;

}

.props-row {
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;

  flex-direction: row;
  flex-flow: row wrap;

  -webkit-flex-flow: row wrap;
  justify-content: center;
  align-items: stretch;

}

.prop-container {
  display: flex;
  justify-content: center;
}

.shop-drawer {
  background-color: rgb(0,0,0) !important;
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
  transition-timing-function: linear;
}

.slide-fade-enter-active {
  transition: all .3s ease;
}

.slide-fade-leave-active {
  transition: all .2s ease;
}

.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}
</style>
