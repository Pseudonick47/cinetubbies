<template>
  <div
    style="width: 100%; height: 100%"
  >
    <v-navigation-drawer
      v-model="drawer"
      class="shop-drawer pl-2 pt-4"
      app
      right
    >
      <div class="px-3">
        <div style="display: flex; justify-content: center">
          <v-btn
            class="mb-3"
            color="primary"
            small
            light
            @click="showCreateDialog = true"
          >New Prop</v-btn>
        </div>
      </div>
      <div class="headline pa-3">Categories</div>
      <categories
        :collection="rootCategories"
        style="background-color: black"
        @select="categorySelected"
      />
    </v-navigation-drawer>
    <v-container
      class="content-container"
      fluid
    >
      <v-layout
        class="content-container"
        row
      >
        <v-flex
          hidden-sm-and-down
          md1
        />
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
          hidden-sm-and-down
          md1
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
      showCreateDialog: false,
      showDeleteDialog: false,
      entriesPerPage: 9,
      page: 1,
      propToDelete: null,
      propToEdit: null
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
    },
    drawer: {
      set(visible) {
        this.$store.commit('miscellaneous/setDrawer', visible);
      },
      get() {
        return this.$store.getters['miscellaneous/drawer'];
      }
    }
  },
  watch: {
    page() {
      PropsController.requestPage(this.page);
    }
  },
  beforeMount() {
    this.$store.commit('miscellaneous/setDrawer', false);

    CategoriesController.requestCategories();
    PropsController.requestCount();
    PropsController.requestPage(this.page);
  },
  beforeDestroy() {
    this.$store.commit('miscellaneous/setDrawer', null);
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
      this.$store.commit('props/deleteProp', this.propToDelete.id);
      this.propToDelete = null;
    }
  }
};
</script>
<style>

.shop-drawer {
  background-color: rgb(0,0,0) !important;
}

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
