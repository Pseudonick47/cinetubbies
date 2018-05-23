<template>
  <div style="height: 100%; width: 100%">
    <v-container
      mt-5
      pt-5
    >
      <v-layout
        v-for="reservation in reservations"
        :key="reservation.id"
        row
        justify-center
      >
        <v-flex
          xs10
          md8
          mb-8
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
                      @click="goToProp(reservation.prop)"
                    >
                      <h3 class="headline">{{ reservation.prop.title }}</h3>
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
                      <h4>{{ summerize(reservation.prop) }}</h4>
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
                      <div class="headline text-xs-center">{{ reservation.quantity }}</div>
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
                  @click="reservationToEdit = reservation; showEditDialog = true"
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
                  @click="reservationToCancel = reservation; showCancelDialog = true"
                >Delete</v-btn>
              </v-flex>
            </v-layout>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
    <simple-dialog
      v-if="showCancelDialog"
      title="Please confirm your decesion to cancel this reservation."
      @cancel="showCancelDialog = false; reservationToCancel = null"
      @confirm="cancelReservation"
    />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import ReservationsController from 'Controllers/props/reservations.controller';
import SimpleDialog from 'Components/helpers/SimpleDialog.component';

export default {
  name: 'PropReservations',
  components: {
    SimpleDialog
  },
  data() {
    return {
      showCancelDialog: false,
      showEditDialog: false,
      reservationToCancel: null,
      reservationToEdit: null
    };
  },
  computed: {
    ...mapGetters('props/reservations/', {
      reservations: 'all'
    }),
    ...mapGetters({
      user: 'activeUser'
    })
  },
  beforeMount() {
    ReservationsController.requestReservationsByUser(this.user.id);
  },
  methods: {
    goToProp(prop) {
      this.$router.push({ name: 'fan-zone-prop', params: { id: prop.id } });
    },
    cancelReservation() {
      ReservationsController.cancelReservation(this.user.id, this.reservationToCancel.id)
        .then(() => {
          this.$alert.success('Reservation is canceled!');
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
