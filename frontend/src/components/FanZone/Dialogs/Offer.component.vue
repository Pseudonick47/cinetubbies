<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="400px"
  >
    <v-card color="black">
      <v-card-title class="headline">How much money would you like to offer?</v-card-title>
      <v-layout
        justify-center
        row
        py-3
        px-4
      >
        <v-flex
          justify-center
          align-center
          xs6
        >
          <v-text-field
            v-validate="'required|decimal:3'"
            ref="amountInput"
            v-model="amount"
            :error-messages="errors.collect('amount')"
            name="amount"
            prefix="$"
            required
            autofocus
          />
        </v-flex>
      </v-layout>
      <v-card-actions>
        <v-layout
          row
          wrap
          justify-space-around
        >
          <v-btn
            class="highlight"
            flat="flat"
            @click="cancel"
          >Cancel</v-btn>
          <v-btn
            class="highlight"
            flat="flat"
            @click="confirm"
          >Confirm</v-btn>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapGetters } from 'vuex';

import OffersController from 'Controllers/props/offers.controller';

import { Prop } from 'Models/prop.model';

export default {
  name: 'Offer',
  props: {
    prop: {
      type: Prop,
      required: true
    }
  },
  data() {
    return {
      show: true,
      amount: 0
    };
  },
  computed: {
    ...mapGetters({
      user: 'activeUser'
    })
  },
  mounted() {
    this.$refs.amountInput.$el.focus();
  },
  methods: {
    cancel() {
      this.show = false;
      this.$emit('cancel');
    },
    confirm() {
      const data = { amount: this.amount };

      OffersController.offer(this.prop.id, data)
        .then((response) => {
          this.$alert.success('You have successfully made an offer!');
          this.$emit('confirm');
        })
        .catch(() => {
          this.$alert.error('Something went wrong. Please try again!');
        });

      this.cancel();
    }
  }
};
</script>
<style>
.highlight {
  color: #daa520 !important;
}
</style>
