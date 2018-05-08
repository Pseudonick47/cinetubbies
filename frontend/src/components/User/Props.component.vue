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
              style="padding: 0 !important"
              clipped
            >
              <h1 class="pa-3 prop-info-highlight">My Props</h1>
              <v-btn
                flat
                block
                @click="dialog=true"
              >
                New Prop
              </v-btn>
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
              <!-- <categories
                :collection="rootCategories"
                @select="categorySelected"
              /> -->
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
        <v-flex>
          <v-container py-5>
            <v-layout
              v-for="prop in props"
              :key="prop.id"
              row
              wrap
              justify-center
              mb-4
            >
              <v-card
                class="prop-info-card grow-card"
                color="black"
              >
                <v-container pa-0>
                  <v-layout
                    row
                    wrap
                  >
                    <v-flex
                      xs12
                      sm12
                      md4
                    >
                      <v-card-media
                        contain
                        height="100%"
                        :src="prop.image.path"
                        style="-webkit-mask-image:-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,1)), to(rgba(0,0,0,0.5)));"
                      />
                    </v-flex>
                    <v-flex
                      xs12
                      sm12
                      md8
                    >
                      <v-container class="prop-info-body">
                        <v-layout
                          row
                          wrap
                        >
                          <v-card-title
                            class="prop-info-item"
                            primary-title
                          >
                            <v-layout
                              row
                              wrap
                              justify-space-between
                              pr-3
                            >
                              <div class="display-1">{{ prop.title }}</div>
                              <v-icon
                                v-if="!prop.approved && prop.pendingApproval"
                                class="prop-info-highlight"
                              >
                                hourglass_empty
                              </v-icon>
                              <v-icon
                                v-else-if="!prop.approved && !prop.pendingApproval"
                                class="prop-info-highlight"
                              >
                                report
                              </v-icon>
                              <v-icon
                                v-else
                                class="prop-info-highlight"
                              >
                                done_all
                              </v-icon>
                            </v-layout>
                          </v-card-title>
                        </v-layout>
                        <v-divider class="prop-info-divider mt-1 mb-3"/>
                        <v-layout
                          class="prop-info-item"
                          row
                          wrap
                          px-4
                          py-1
                          mb-0
                        >
                          <div class="subheading">
                            <p style="text-align: justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor felis at mollis blandit. Etiam quam dui, pharetra ac ligula ut, varius venenatis metus. Curabitur eget efficitur nisi. Proin commodo efficitur tortor vel vulputate. Nam ipsum dolor, pulvinar at vehicula sit amet, porttitor a nisi. Donec congue tristique justo ac fringilla.</p>
                          </div>
                          <div
                            class="caption grey--text"
                            style="width: 100%"
                          >
                            <p class="text-xs-right">Expiration date: {{ prop.expirationDate }}</p>
                          </div>
                        </v-layout>
                        <v-layout
                          row
                          wrap
                        >
                          <v-card-actions
                            class="prop-info-item"
                          >
                            <v-layout
                              row
                              wrap
                              justify-end
                            >
                              <v-btn
                                class="prop-info-highlight"
                                flat
                              >
                                Edit
                              </v-btn>
                              <v-btn
                                class="prop-info-highlight"
                                flat
                              >
                                Remove
                              </v-btn>
                            </v-layout>
                          </v-card-actions>
                        </v-layout>
                      </v-container>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card>
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
        </v-flex>
        <v-flex
          xs2
          sm1
        />
      </v-layout>
    </v-container>
    <used-prop-dialog
      v-if="dialog"
      @close="dialog=false"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import UsedPropDialog from 'Components/User/UsedPropDialog.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/used-props.controller';

export default {
  name: 'UserProps',
  components: {
    UsedPropDialog
  },
  data() {
    return {
      drawer: true,
      dialog: false,
      approved: true,
      pendingApproval: false,
      submited: true,
      entriesPerPage: 10,
      page: 1
    };
  },
  computed: {
    ...mapGetters('props/used/', {
      props: 'all',
      count: 'count'
    }),
    ...mapGetters('props/categories/', {
      rootCategories: 'roots',
      categoryPath: 'path'
    }),
    ...mapGetters({
      user: 'activeUser'
    }),
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    }
  },
  watch: {
    page() {
      PropsController.requestPage(this.page, { user: this.user.id });
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    PropsController.requestCount({ user: this.user.id });
    PropsController.requestPage(this.page, { user: this.user.id });
  },
  methods: {
    categorySelected(id) {
      if (id === -1) {
        PropsController.requestCount();
        PropsController.requestPage(this.page);
      } else {
        payload = {
          category: id,
          user: this.user.id
        };

        PropsController.requestCount(payload);
        PropsController.requestPage(this.page, payload);
      }
    }
  }
};
</script>
<style>
.content-container {
  padding: 0;
  height: 100%;
  transition-timing-function: linear;
}

.prop-info-background {
  color: rgb(27, 25, 25);
}

.prop-info-card {
  background: linear-gradient(90deg, black, #030303, #080808, #101010);
  width: 75%;
}

.prop-info-card:hover {
  box-shadow: 0px 0px 5px #daa520;
}

.prop-info-body {
  height: 100% !important;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-content: space-between;
}

.prop-info-item {
  width: 100%;
}

.prop-info-highlight {
  color: #daa520 !important;
}

.prop-info-divider {
  background: linear-gradient(90deg, black, #424242, #c5951b, #424242, black);
}

.grow-card {
  transition: all .2s ease-in-out;
}

.grow-card:hover {
  transform: scale(1.05);
}

</style>

