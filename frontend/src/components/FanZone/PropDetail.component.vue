<template>
  <v-dialog
    v-model="show"
    max-width="900px"
  >
    <v-card>
      <v-card-title>
        Dialog 2
      </v-card-title>
      <v-card-text>
        Some text
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="primary"
          flat
          @click.stop="show=false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'PropDetail',
  data() {
    return {
      show: true
    };
  },
  watch: {
    show() {
      if (!this.show) {
        this.$emit('close');
      }
    }
  }
};
</script>
