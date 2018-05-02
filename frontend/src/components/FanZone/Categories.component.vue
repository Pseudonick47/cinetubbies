<template>
  <div>
    <category
      v-for="(cat, i) in collection"
      :key="i"
      :info="cat"
      @select="select"
    />
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
