<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="400px"
  >
    <v-card color="black">
      <v-card-title class="headline">{{ title }}</v-card-title>
      <v-card-text v-if="text">{{ text }}</v-card-text>
      <v-card-actions>
        <v-layout
          row
          wrap
          justify-space-between
          py-1
        >
          <v-btn
            class="highlight"
            flat="flat"
            @click="cancel"
          >Cancel</v-btn>
          <v-btn
            class="highlight"
            flat="flat"
            @click="confirm"
          >Confirm</v-btn>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'SimpleDialog',
  props: {
    title: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: false,
      default: () => ''
    },
    payload: {
      type: Object,
      required: false,
      default: () => {}
    }
  },
  data() {
    return {
      show: true
    };
  },
  methods: {
    cancel() {
      this.show = false;
      this.$emit('cancel');
    },
    confirm() {
      this.$emit('confirm', this.payload);
      this.cancel();
    }
  }
};
</script>
<style>
.highlight {
  color: #daa520 !important;
}
</style>
