<template>
  <div class="background">
    <v-container fluid>
      <v-layout
        row
        wrap
      >
        <v-flex
          xs12
          sm12
          md4
        >
          <img
            :src="prop.image.path"
            alt="Prop image"
            style="object-fit: contain"
          >
        </v-flex>
        <v-flex
          xs12
          sm12
          md8
        >
          <v-container>
            <v-layout row>
              {{ prop.title }}
            </v-layout>
            <v-layout row>
              {{ prop.description }}
            </v-layout>
            <v-layout row>
              <v-btn
                v-if="showReserveBtn"
                flat
                @click="showReserveDialog = true"
              >Reserve</v-btn>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-container>
    <reserve-prop-dialog
      v-if="showReserveDialog"
      :prop="prop"
      @cancel="showReserveDialog = false"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import ReservePropDialog from 'Components/FanZone/Dialogs/ReserveProp.component';

export default {
  name: 'PropDetail',
  components: {
    ReservePropDialog
  },
  props: {
    id: {
      type: [ Number, String ],
      required: true
    }
  },
  data() {
    return {
      prop: null,
      showReserveDialog: false
    };
  },
  computed: {
    ...mapGetters({
      user: 'activeUser'
    }),
    showReserveBtn() {
      return this.prop.isOfficial() && this.user && this.prop.quantity > 0;
    }
  },
  beforeMount() {
    this.prop = this.$store.getters['props/one'](Number(this.id));
  }
};
</script>
<style>

.backgroud {
  background-color: black;
  height: 100%;
}

</style>
