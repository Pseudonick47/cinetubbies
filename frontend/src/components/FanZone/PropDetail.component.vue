<template>
  <div class="background">
    <v-container fluid>
      <v-layout
        v-if="prop"
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
import PropsController from 'Controllers/props/props.controller';

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
      showReserveDialog: false
    };
  },
  computed: {
    ...mapGetters({
      user: 'activeUser'
    }),
    showReserveBtn() {
      return this.prop.isOfficial() && this.user && this.prop.quantity > 0;
    },
    prop() {
      console.log('here');
      return this.$store.getters['props/get'];
    }
  },
  beforeMount() {
    PropsController.requestOne(this.id);
  }
};
</script>
<style>

.backgroud {
  background-color: black;
  height: 100%;
}

</style>
