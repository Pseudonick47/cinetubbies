<template>
  <div class="prop-detail-container">
    <v-card class="prop-detail">
      <v-container
        v-if="prop"
        pa-0
        fill-height
      >
        <v-layout
          row
          wrap
          px-3
        >
          <v-flex
            xs12
            sm12
            md5
          >
            <v-card-media
              v-if="prop.image"
              :src="prop.image.path"
              contain
              height="100%"
              style="-webkit-mask-image:-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,1)), to(rgba(0,0,0,0.5)));"
            />
          </v-flex>
          <v-flex
            xs12
            sm12
            md7
          >
            <v-container class="prop-info-body">
              <v-card-title pa-4>
                <div class="display-1 pa-1">{{ prop.title }}</div>
              </v-card-title>
              <v-divider class="prop-info-divider mt-1 mb-3"/>
              <v-layout
                class="prop-info-item"
                row
                wrap
                px-4
                py-1
                mb-0
              >
                <div class="subheading">
                  <p style="text-align: justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor felis at mollis blandit. Etiam quam dui, pharetra ac ligula ut, varius venenatis metus. Curabitur eget efficitur nisi. Proin commodo efficitur tortor vel vulputate. Nam ipsum dolor, pulvinar at vehicula sit amet, porttitor a nisi. Donec congue tristique justo ac fringilla.</p>
                </div>
              </v-layout>
              <v-layout
                row
                wrap
                style="height: auto"
                pb-4
                pr-3
                justify-end
              >
                <v-flex xs3>
                  <v-btn
                    v-if="showBookBtn"
                    flat
                    color="primary"
                    @click="showBookDialog = true"
                  >Book</v-btn>
                  <v-btn
                    v-if="showOfferBtn"
                    flat
                    color="primary"
                    @click="showOfferDialog = true"
                  >Offer</v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
    <book-dialog
      v-if="showBookDialog"
      :prop="prop"
      @cancel="showBookDialog = false"
      @confirm="showBookDialog = false"
    />
    <offer-dialog
      v-if="showOfferDialog"
      :prop="prop"
      @cancel="showOfferDialog = false"
      @confirm="showOfferDialog = false"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import BookDialog from 'Components/FanZone/Dialogs/BookProp.component';
import OfferDialog from 'Components/FanZone/Dialogs/Offer.component';
import PropsController from 'Controllers/props/props.controller';

export default {
  name: 'PropDetail',
  components: {
    BookDialog,
    OfferDialog
  },
  props: {
    id: {
      type: [ Number, String ],
      required: true
    }
  },
  data() {
    return {
      showBookDialog: false,
      showOfferDialog: false
    };
  },
  computed: {
    ...mapGetters({
      user: 'activeUser'
    }),
    showBookBtn() {
      if (!this.prop.isOfficial()) {
        return false;
      }
      return this.user && !this.user.isAnyAdmin() && this.prop.quantity > 0;
    },
    showOfferBtn() {
      if (!this.prop.isUsed()) {
        return false;
      }
      return this.user && !this.user.isAnyAdmin() &&
             this.prop.owner.id != this.user.id;
    },
    prop() {
      return this.$store.getters['props/get'];
    }
  },
  beforeMount() {
    PropsController.requestOne(this.id);
  }
};
</script>
<style>

.prop-detail-container {
  height: 100%;
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: center;
}

.prop-detail {
  height: 80% !important;
  width: 65%;
  background-color: black !important;
}

.prop-detail-img-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.prop-detail-img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}

.prop-detail-description {
  /* height: 100%; */
  /* width: 100%; */
  /* background: linear-gradient(90deg, black, rgb(16, 16, 16), rgb(24, 24, 24)); */
  background-color: black;
}

</style>
