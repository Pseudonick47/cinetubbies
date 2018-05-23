<template>
  <div style="height: 100%; width: 100%;">
    <v-container>
      <v-layout
        v-for="offer in offers"
        :key="offer.id"
        row
        justify-center
      >
        <v-flex
          xs8
          md6
          mb-3
        >
          <v-card>
            <v-layout
              row
              wrap
            >
              <v-flex
                xs8
              >
                <v-layout
                  row
                  wrap
                  justify-start
                >
                  <v-flex align-center>
                    <v-card-title
                      style="cursor: pointer"
                      @click="goToProp(offer.prop)"
                    >
                      <h3 class="headline">{{ offer.prop.title }}</h3>
                    </v-card-title>
                  </v-flex>
                  <v-flex
                    align-center
                    d-flex
                  >
                    <v-card-text>
                      Amount: {{ offer.amount }}
                    </v-card-text>
                  </v-flex>
                  <v-spacer />
                </v-layout>
              </v-flex>
              <v-flex
                xs4
                align-center
                d-flex
              >
                <v-layout
                  row
                  wrap
                  justify-end
                >
                  <v-btn
                    flat
                    @click="offerToEdit = offer; showEditDialog = true"
                  >Edit</v-btn>
                  <v-btn
                    flat
                    @click="offerToDelete = offer; showDeleteDialog = true"
                  >Delete</v-btn>
                </v-layout>
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
      :prop="prop"
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
        .then(() => {
          this.$alert.success('Offer deleted!');
        })
        .catch(() => {
          this.$alert.error('Something went wrong. Please try again!');
        });
    }
  }
};
</script>
