<template>
  <div>
    <!-- <category
      v-for="(cat, i) in collection"
      :key="i"
      :info="cat"
      @select="select"
    /> -->
    <v-list>
      <v-list-tile
        @click="select(-1)"
      >
        <v-list-tile-title>Display All Props</v-list-tile-title>
      </v-list-tile>
      <template v-for="(cat, i) in collection">
        <v-list-group
          v-if="cat.subcategories"
          :key="i"
        >
          <v-list-tile slot="activator">
            <v-list-tile-title>{{ cat.name }}</v-list-tile-title>
          </v-list-tile>
          <v-list-tile
            v-for="(subcat, j) in cat.subcategories"
            :key="j"
            @click="select(subcat.id)"
          >
            <v-list-tile-title>{{ subcat.name }}</v-list-tile-title>
          </v-list-tile>
        </v-list-group>
        <v-list-tile
          v-else
          :key="i"
          @click="select(cat.id)"
        >
          <v-list-tile-title>{{ cat.name }}</v-list-tile-title>
        </v-list-tile>
      </template>
    </v-list>
  </div>
</template>
<script>
import Category from 'Components/FanZone/Category.component';

export default {
  name: 'Categories',
  components: {
    Category
  },
  props: {
    collection: {
      type: Array,
      required: true
    }
  },
  created() {
    this.$emit('created');
  },
  methods: {
    select(id) {
      this.$emit('select', id);
    }
  }
};
</script>
