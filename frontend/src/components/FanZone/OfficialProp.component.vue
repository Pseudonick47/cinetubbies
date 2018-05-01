<template>
  <v-card class="theater-card">
    <v-card-title primary-title>
      <div>
        <div class="headline">{{ info.title }}</div>
        <span class="grey--text">{{ category.name }}</span>
      </div>
    </v-card-title>
    <v-card-text>
      {{ info.description }}
    </v-card-text>
    <v-card-actions>
      <v-layout
        row
        justify-space-between
      >
        <v-btn
          flat
          @click="edit"
        >
          Edit
        </v-btn>
        <v-btn
          flat
          color="purple"
          @click="remove"
        >
          Remove
        </v-btn>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'OfficialProp',
  props: {
    info: {
      type: Object,
      required: true
    }
  },
  computed: {
    category() {
      return this.$store.getters['props/categories/one'](this.info.category);
    }
  },
  methods: {
    edit() {
      this.$emit('edit');
    },
    remove() {
      this.$emit('remove');
    }
  }
};
</script>
