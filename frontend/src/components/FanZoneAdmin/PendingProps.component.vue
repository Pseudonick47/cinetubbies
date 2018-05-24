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
          hidden-sm-and-down
          md1
        />
      </v-layout>
    </v-container>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import Categories from 'Components/FanZone/Categories.component';
import PropControl from 'Components/FanZone/PropControl.component';

import CategoriesController from 'Controllers/props/categories.controller';
import PropsController from 'Controllers/props/used-props.controller';

export default {
  name: 'PendingProps',
  components: {
    Categories,
    PropControl
  },
  data() {
    return {
      drawer: true,
      entriesPerPage: 10,
      page: 1
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
      PropsController.requestPage(this.page, { approved: true });
    }
  },
  beforeMount() {
    CategoriesController.requestCategories();
    PropsController.requestCount({ approved: true });
    PropsController.requestPage(this.page, { approved: true });
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
      const { prop, action } = payload;

      const decision = action === 'approve';

      PropsController.reviewProp(prop.id, { approve: decision })
        .then((response) => {
          this.$alert.success('Prop successfully reviewed.');

          PropsController.requestCount({ approved: false });
          PropsController.requestPage(this.page, { approved: false });
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

