<template>
  <v-expansion-panel
    class="elevation-0"
  >
    <v-expansion-panel-content
      v-if="hasChildren"
      ripple
    >
      <div
        slot="header"
      >
        {{ info.name }}
      </div>
      <categories
        :collection="info.subcategories"
        class="pl-4"
        @select="propagetSelect"
      />
    </v-expansion-panel-content>
    <v-expansion-panel-content
      v-else
      hide-actions
      ripple
    >
      <div
        slot="header"
        @click.stop="select"
      >
        {{ info.name }}
      </div>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>
<script>
import * as _ from 'lodash';

export default {
  name: 'Category',
  props: {
    info: {
      type: Object,
      required: true
    }
  },
  computed: {
    hasChildren() {
      return !_.isEmpty(this.info.subcategories);
    }
  },
  beforeCreate() {
    this.$options.components.Categories = require('./Categories.component.vue').default;
  },
  methods: {
    propagetSelect(id) {
      this.$emit('select', id);
    },
    select() {
      this.$emit('select', this.info.id);
    }
  }
};
</script>
