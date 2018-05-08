<template>
  <div>
    <v-container
      class="content-container"
      fluid
    >
      <v-layout
        class="content-container"
        row
      >
        <transition name="slide-fade">
          <v-flex
            v-if="drawer"
            sm2
          >
            <v-navigation-drawer
              v-model="drawer"
              class="pl-2"
              clipped
            >
              <h1 class="pa-3 mb-3">Fan Zone</h1>
              <div class="pl-3">
                <v-switch
                  v-model="showOfficialProps"
                  label="Official props"
                />
                <v-switch
                  v-model="showUsedProps"
                  label="Used props"
                />
              </div>
              <h2 class="pa-3">Categories</h2>
              <v-expansion-panel class="elevation-0">
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
                @select="categorySelected"
              />
            </v-navigation-drawer>
          </v-flex>
        </transition>
        <v-flex
          xs2
          sm1
          style="display: flex; align-items: center;"
        >
          <v-btn
            fab
            small
            color="black"
            style="transform: scale(0.8);"
            @click="drawer = !drawer"
          >
            <v-icon>keyboard_arrow_left</v-icon>
          </v-btn>
        </v-flex>
        <v-flex style="display: flex; flex-direction: column;">
          <div style="overflow: auto;">
            <v-container style="align-items: stretch;">
              <v-layout
                row
                pa-2
                justify-center
                mb-5
              >
                <v-card class="props-toolbar">
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
                v-for="i in 3"
                :key="i"
                class="props-row"
                row
              >
                <v-flex
                  xs12
                  sm6
                  md4
                  lg3
                  xl3
                  pa-3
                  @click="dialog=true"
                >
                  <used-prop @click="dialog=true"/>
                </v-flex>
                <v-flex
                  xs12
                  sm6
                  md4
                  lg3
                  xl3
                  pa-3
                >
                  <used-prop />
                </v-flex>
                <v-flex
                  xs12
                  sm6
                  md4
                  lg3
                  xl3
                  pa-3
                >
                  <used-prop />
                </v-flex>
                <v-flex
                  xs12
                  sm6
                  md4
                  lg3
                  xl3
                  pa-3
                >
                  <used-prop />
                </v-flex>
                <!-- <v-flex
                  v-for="entry in entries"
                  :key="entry.id"
                  xs12
                  sm6
                  md4
                  lg4
                  xl4
                  pa-3
                > -->
                <!-- <official-prop
                  :info="entry"
                /> -->
                <!-- </v-flex> -->
              </v-layout>
            </v-container>
            <v-container
              id="pagination"
              style="display: flex; flex-direction: column; align-items: center;"
            >
              <v-layout

              >
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
          xs2
          sm1
        />
      </v-layout>
    </v-container>
    <used-prop-detail
      v-if="dialog"
      @close="dialog=false"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import OfficialProp from 'Components/FanZone/OfficialProp.component';
import UsedProp from 'Components/FanZone/UsedProp.component';
import UsedPropDetail from 'Components/FanZone/UsedPropDetail.component';
import CategoriesController from 'Controllers/props/categories.controller';
import OfficialPropsController from 'Controllers/props/official-props.controller';
import UsedPropsController from 'Controllers/props/used-props.controller';

import * as _ from 'lodash';

export default {
  name: 'FanZoneHome',
  components: {
    Categories,
    OfficialProp,
    UsedProp,
    UsedPropDetail
  },
  data() {
    return {
      drawer: true,
      dialog: false,
      entriesPerPage: 9,
      page: 1,
      theater: 2,
      showOfficialProps: true,
      showUsedProps: false
    };
  },
  computed: {
    ...mapGetters('props/official/', {
      officialProps: 'all',
      officialPropCount: 'count'
    }),
    ...mapGetters('props/used/', {
      usedProps: 'all',
      usedPropCount: 'count'
    }),
    ...mapGetters('props/categories/', {
      rootCategories: 'roots',
      categoryPath: 'path'
    }),
    props() {

    },
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    }
  },
  watch: {
    page() {
      OfficialPropsController.requestPage(this.page);
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    OfficialPropsController.requestCount();
    OfficialPropsController.requestPage(this.page);
  },
  methods: {
    categorySelected(id) {
      if (id === -1) {
        OfficialPropsController.requestCount();
        OfficialPropsController.requestPage(this.page);
      } else {
        OfficialPropsController.requestCount({ category: id });
        OfficialPropsController.requestPage(this.page, { category: id });
      }
    }
  }
};
</script>
<style>
.props-toolbar {
  width: 70%;
}
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
