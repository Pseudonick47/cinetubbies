<template>
  <div>
    <v-navigation-drawer
      v-model="drawer"
      app
      right
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
      <categories
        :collection="rootCategories"
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
                status
                @clicked="propClicked"
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
    <used-prop-dialog
      v-if="dialog"
      @close="dialog=false"
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

import PropControl from 'Components/FanZone/PropControl.component';
import Categories from 'Components/FanZone/Categories.component';
import UsedPropDialog from 'Components/User/UsedPropDialog.component';
import SimpleDialog from 'Components/helpers/SimpleDialog.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/used-props.controller';

export default {
  name: 'UserProps',
  components: {
    PropControl,
    UsedPropDialog,
    Categories,
    SimpleDialog
  },
  data() {
    return {
      drawer: true,
      dialog: false,
      approved: true,
      pendingApproval: false,
      submited: true,
      entriesPerPage: 10,
      page: 1,
      propToDelete: null,
      showDeleteDialog: false
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
    ...mapGetters({
      user: 'activeUser'
    }),
    pageCount() {
      return _.ceil(_.divide(this.count, this.entriesPerPage));
    }
  },
  watch: {
    page() {
      PropsController.requestPage(this.page, { user: this.user.id, all: true });
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    PropsController.requestCount({ user: this.user.id, all: true });
    PropsController.requestPage(this.page, { user: this.user.id, all: true });
  },
  methods: {
    categorySelected(id) {
      const payload = {
        user: this.user.id,
        all: true
      };

      if (id !== -1) {
        payload.category = id;
      }

      PropsController.requestCount(payload);
      PropsController.requestPage(this.page, payload);
    },
    propClicked(payload) {
      const { prop, action } = payload;

      if (action === 'delete') {
        this.propToDelete = prop;
        this.showDeleteDialog = true;
      }
    },
    deleteProp() {
      const id = this.propToDelete.id;

      this.propToDelete = null;
      this.showDeleteDialog = false;

      PropsController.deleteProp(id).then(() => {
        this.$store.commit('props/deleteProp', id);
      });
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

