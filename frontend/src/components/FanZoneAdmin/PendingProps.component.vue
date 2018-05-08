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
              <used-prop
                :info="prop"
                :actions="['approve', 'reject']"
                @clicked="changePropStatus"
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
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import UsedProp from 'Components/FanZone/UsedProp.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/used-props.controller';

export default {
  name: 'PendingProps',
  components: {
    Categories,
    UsedProp
  },
  data() {
    return {
      drawer: true,
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
      PropsController.requestPage(this.page, { approved: false });
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    PropsController.requestCount({ approved: false });
    PropsController.requestPage(this.page, { approved: false });
  },
  methods: {
    categorySelected(id) {
      const payload = {
        approved: false
      };

      if (id !== -1) {
        payload.category = id;
      }

      PropsController.requestCount(payload);
      PropsController.requestPage(this.page, payload);
    },
    changePropStatus(payload) {
      const { id, action } = payload;

      const decision = action === 'approve';

      PropsController.reviewProp(id, { approve: decision })
        .then((response) => {
          this.$alert.success('Prop successfully reviewed.');

          PropsController.requestCount({ approved: false });
          PropsController.requestPage(this.page, { approved: false });
        })
        .catch((error) => {
          console.log(error);
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

