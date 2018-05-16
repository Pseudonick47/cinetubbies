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
                @click="showCreateDialog = true"
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
              <prop-control
                :prop="prop"
                :actions="['edit', 'delete']"
                @clicked="mutateProp"
              />
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
        </v-flex>
        <v-flex
          xs2
          sm1
        />
      </v-layout>
    </v-container>
    <official-prop-dialog
      v-if="showCreateDialog && propToEdit"
      :prop="propToEdit"
      @close="showCreateDialog = false; propToEdit = null"
    />
    <official-prop-dialog
      v-else-if="showCreateDialog"
      @close="showCreateDialog = false; propToEdit = null"
    />
    <simple-dialog
      v-if="showDeleteDialog"
      title="Please confirm your decesion to delete this prop."
      text="This action is irreversible. Prop will be removed from the store and all reservations will be canceled."
      @cancel="showDeleteDialog = false; propToDelete = null"
      @confirm="deleteProp"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import PropControl from 'Components/FanZone/PropControl.component';
import OfficialPropDialog from 'Components/FanZoneAdmin/OfficialPropDialog.component';
import SimpleDialog from 'Components/helpers/SimpleDialog.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/official-props.controller';

export default {
  name: 'FanZoneAdminHome',
  components: {
    Categories,
    PropControl,
    OfficialPropDialog,
    SimpleDialog
  },
  data() {
    return {
      drawer: true,
      showCreateDialog: false,
      showDeleteDialog: false,
      entriesPerPage: 9,
      page: 1,
      propToDelete: null,
      propToEdit: null
    };
  },
  computed: {
    ...mapGetters('props/official/', {
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
    categorySelected(id) {
      if (id !== -1) {
        PropsController.requestCount({ category: id });
        PropsController.requestPage(this.page, { category: id });
      } else {
        PropsController.requestCount();
        PropsController.requestPage(this.page);
      }
    },
    mutateProp(payload) {
      const { prop, action } = payload;
      if (action === 'delete') {
        this.propToDelete = prop;
        this.showDeleteDialog = true;
      } else if (action === 'edit') {
        this.propToEdit = prop.clone();
        this.showCreateDialog = true;
      }
    },
    deleteProp() {
      this.showDeleteDialog = false;
      PropsController.deleteProp(this.propToDelete.id);
      this.$store.commit('props/official/deleteProp', this.propToDelete.id);
      this.propToDelete = null;
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
