<template>
  <div>
    <v-container>
      <v-layout
        v-for="reservation in reservations"
        :key="reservation.id"
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
                      @click="goToProp(reservation.prop)"
                    >
                      <h3 class="headline">{{ reservation.prop.title }}</h3>
                    </v-card-title>
                  </v-flex>
                  <v-flex
                    align-center
                    d-flex
                  >
                    <v-card-text>
                      Quantity: {{ reservation.quantity }}
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
                    @click="reservationToCancel = reservation; showCancelDialog = true"
                  >Cancel</v-btn>
                </v-layout>
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
      reservationToCancel: null
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
    }
  }
};
</script>
