<template>
  <v-card
    class="theater-card"
    color="black"
  >
    <v-card-title primary-title>
      <div>
        <div class="headline">{{ info.username }}</div>
        <span class="grey--text">{{ info.email }}</span>
      </div>
    </v-card-title>
    <v-card-actions>
      <v-layout
        row
        justify-space-between
      >
        <v-btn
          flat
          color="primary"
          @click="edit"
        >
          Edit
        </v-btn>
        <v-btn
          flat
          color="primary"
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
  name: 'Admin',
  props: {
    info: {
      type: Object,
      required: true
    }
  },
  methods: {
    edit() {
      this.$emit('editAdmin', this.info.id);
    },
    remove() {
      this.$emit('removeAdmin', this.info.id);
    }
  }
};
</script>

<style>

.theater-card {
  height: 100% !important;
  justify-content: space-between;
  flex-direction: column;
  display: flex;
}

</style>
