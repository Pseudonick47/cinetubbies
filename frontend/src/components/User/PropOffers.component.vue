<template>
  <div style="height: 100%; width: 100%;">
    <v-container
      mt-5
      pt-5
    >
      <v-layout
        v-for="offer in offers"
        :key="offer.id"
        row
        justify-center
        mt-3
      >
        <v-flex
          sm10
          md8
          mb-3
        >
          <v-card color="black">
            <v-layout
              row
              wrap
            >
              <v-flex
                xs12
                sm12
                md8
              >
                <v-layout
                  class="height-auto"
                  row
                  wrap
                  justify-start
                >
                  <v-flex align-center>
                    <v-card-title
                      class="pb-1"
                      style="cursor: pointer"
                      @click="goToProp(offer.prop)"
                    >
                      <h3 class="headline">{{ offer.prop.title }}</h3>
                    </v-card-title>
                  </v-flex>
                </v-layout>
                <v-layout
                  class="height-auto"
                  row
                  wrap
                  justify-start
                  pl-4
                >
                  <v-flex align-center>
                    <v-card-text style="padding-bottom: 0;">
                      <h4>{{ summerize(offer.prop) }}</h4>
                    </v-card-text>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex
                xs12
                sm12
                md4
              >
                <v-layout
                  row
                  wrap
                  align-center
                >
                  <v-flex>
                    <v-card-title style="display: flex; justify-content: center;">
                      <div class="headline text-xs-center">{{ offer.amount }}$</div>
                    </v-card-title>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
            <v-layout
              row
              wrap
              justify-end
            >
              <v-flex
                xs2
                align-center
              >
                <v-btn
                  flat
                  block
                  color="primary"
                  @click="offerToEdit = offer; showEditDialog = true"
                >Edit</v-btn>
              </v-flex>
              <v-flex
                xs2
                align-center
              >
                <v-btn
                  flat
                  block
                  color="primary"
                  @click="offerToDelete = offer; showDeleteDialog = true"
                >Delete</v-btn>
              </v-flex>
            </v-layout>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
    <simple-dialog
      v-if="showDeleteDialog"
      title="Please confirm your decesion to delete this offer."
      @cancel="showDeleteDialog = false; offerToDelete = null"
      @confirm="deleteOffer"
    />
    <offer-dialog
      v-if="showEditDialog"
      :offer="offerToEdit"
      :prop="offerToEdit.prop"
      @cancel="showEditDialog = false"
      @confirm="showEditDialog = false"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import OfferDialog from 'Components/FanZone/Dialogs/Offer.component';
import SimpleDialog from 'Components/helpers/SimpleDialog.component';

import OffersController from 'Controllers/props/offers.controller';

export default {
  name: 'PropOffers',
  components: {
    OfferDialog,
    SimpleDialog
  },
  data() {
    return {
      showDeleteDialog: false,
      showEditDialog: false,
      offerToDelete: null,
      offerToEdit: null
    };
  },
  computed: {
    ...mapGetters('props/offers/', {
      offers: 'all'
    }),
    ...mapGetters({
      user: 'activeUser'
    })
  },
  beforeMount() {
    OffersController.requestOffersByUser(this.user.id);
  },
  methods: {
    goToProp(prop) {
      this.$router.push({ name: 'fan-zone-prop', params: { id: prop.id } });
    },
    deleteOffer() {
      OffersController.deleteOffer(this.user.id, this.offerToDelete.id)
        .then((response) => {
          this.$store.commit('props/offers/delete', response.data.id);
          this.$alert.success('Offer deleted!');
        })
        .catch(() => {
          this.$alert.error('Something went wrong. Please try again!');
        });
    },
    summerize(prop) {
      if (prop.description.length > 32) {
        return `${prop.description.substring(0, 32)}...`;
      }
      return prop.description;
    }
  }
};
</script>
<style>

.height-auto {
  height: auto !important;
}

</style>
