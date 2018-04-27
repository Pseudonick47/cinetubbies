<template>
  <div>
    <v-alert
      :color="alertColor"
      :value="showAlert"
      :icon="alertIcon"
      style="position: fixed; top:0; left: 20%; width: 60%; z-index: 9999; margin: 0;"
      transition="fade-transition"
    >
      {{ alertMessage }}
    </v-alert>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'AlertBox',
  computed: {
    ...mapGetters([
      'alertColor',
      'showAlert',
      'alertMessage',
      'alertIcon'
    ])
  }
};
</script>
