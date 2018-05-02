<template>
  <v-container>
    <v-layout
      justify-center
    >
      <v-flex
        xs12
        sm8
        md6
        align-center
      >
        <v-card
          class="elevation-3"
        >
          <v-card-title
            class="elevation-2"
            primary-title
          >
            <div class="display-1">Reward Scale</div>
          </v-card-title>
          <v-card-text>
            <div class="pa-2">
              <v-form>
                <div class="title">Basic Member</div>
                <v-layout
                  row
                  wrap
                  justify-space-around
                >
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="basic.min"
                      :error-messages="errors.collect('basic-min')"
                      name="basic-min"
                      label="Min"
                    />
                  </v-flex>
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="basic.max"
                      :error-messages="errors.collect('basic-max')"
                      name="basic-max"
                      label="Max"
                    />
                  </v-flex>
                </v-layout>
                <div class="title">Bronze Member</div>
                <v-layout
                  row
                  wrap
                  justify-space-around
                >
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="bronze.min"
                      :error-messages="errors.collect('bronze-min')"
                      name="bronze-min"
                      label="Min"
                    />
                  </v-flex>
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="bronze.max"
                      :error-messages="errors.collect('bronze-max')"
                      name="bronze-max"
                      label="Max"
                    />
                  </v-flex>
                </v-layout>
                <div class="title">Silver Member</div>
                <v-layout
                  row
                  wrap
                  justify-space-around
                >
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="silver.min"
                      :error-messages="errors.collect('silver-min')"
                      name="silver-min"
                      label="Min"
                    />
                  </v-flex>
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="silver.max"
                      :error-messages="errors.collect('silver-max')"
                      name="silver-max"
                      label="Max"
                    />
                  </v-flex>
                </v-layout>
                <div class="title">Gold Member</div>
                <v-layout
                  row
                  wrap
                  justify-space-around
                >
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="gold.min"
                      :error-messages="errors.collect('gold-min')"
                      name="gold-min"
                      label="Min"
                    />
                  </v-flex>
                  <v-flex
                    xs12
                    sm12
                    md5
                  >
                    <v-text-field
                      v-validate="'numeric'"
                      v-model="gold.max"
                      :error-messages="errors.collect('gold-max')"
                      name="gold-max"
                      label="Max"
                    />
                  </v-flex>
                </v-layout>
              </v-form>
            </div>
            <v-layout
              row
              wrap
              justify-space-around
              mt-3
            >
              <v-flex
                xs7
                sm7
                md3
              >
                <v-btn
                  block
                  @click="reset"
                >
                  Reset
                </v-btn>
              </v-flex>
              <v-flex
                xs7
                sm7
                md3
              >
                <v-btn
                  block
                  @click="confirm"
                >
                  Confirm
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import { mapGetters } from 'vuex';

import ReservationsController from 'Controllers/reservations.controller';

export default {
  name: 'SystemAdminRewards',
  computed: {
    ...mapGetters('reservations', [ 'basic', 'bronze', 'silver', 'gold', 'all' ])
  },
  beforeMount() {
    ReservationsController.requestRewards();
  },
  methods: {
    reset() {
      ReservationsController.requestRewards();
    },
    confirm() {
      this.$validator.validateAll().then((result) => {
        if (result) {
          ReservationsController.updateRewards(this.all)
            .then(() => {
              this.$alert.success('Rewards successfully updated!');
            })
            .catch(() => {
              this.$alert.error('Something went wrong! Please try again.');
            });
        } else {
          this.$alert.error('All fileds accept only numeric values!');
        }
      });
    }
  }
};
</script>
