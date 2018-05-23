<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="400px"
  >
    <v-card color="black">
      <v-card-title class="headline">How many items should we make reservations for?</v-card-title>
      <v-layout
        justify-center
        row
        py-3
        px-4
      >
        <v-flex
          justify-end
          xs4
        >
          <v-btn
            :disabled="!decBtn"
            class="highlight"
            flat
            block
            @click="dec"
            @mousedown="repDec"
            @mouseup="repeat = false"
          >
            <v-icon>remove</v-icon>
          </v-btn>
        </v-flex>
        <v-flex
          justify-center
          align-center
          xs2
        >
          <h2
            class="text-xs-center pt-2"
            style="vertical-align: middle; height: 100%"
          >{{ num }}</h2>
        </v-flex>
        <v-flex
          justify-start
          xs4
        >
          <v-btn
            :disabled="!incBtn"
            class="highlight"
            flat
            block
            @click="inc"
            @mousedown="repInc"
            @mouseup="repeat = false"
          >
            <v-icon>add</v-icon>
          </v-btn>
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

import ReservationController from 'Controllers/props/reservations.controller';

import { Prop } from 'Models/prop.model';

export default {
  name: 'BookProp',
  props: {
    prop: {
      type: Prop,
      required: true
    }
  },
  data() {
    return {
      show: true,
      num: 1,
      incBtn: this.prop.quantity != 1,
      decBtn: false,
      repeat: false
    };
  },
  computed: {
    ...mapGetters({
      user: 'activeUser'
    }),
    max() {
      return this.prop.quantity;
    }
  },
  methods: {
    rep(func) {
      window.setTimeout(() => {
        const int = window.setInterval(() => {
          if (this.repeat) {
            func();
          } else {
            window.clearInterval(int);
          }
        }, 150);
      }, 200);
    },
    inc() {
      this.num += 1;
      this.decBtn = true;
      if (this.num >= this.max) {
        this.num = this.max;
        this.repeat = false;
        this.incBtn = false;
      }
    },
    repInc() {
      this.repeat = true;
      this.rep(this.inc);
    },
    dec() {
      this.num -= 1;
      this.incBtn = true;
      if (this.num <= 1) {
        this.num = 1;
        this.repeat = false;
        this.decBtn = false;
      }
    },
    repDec() {
      this.repeat = true;
      this.rep(this.dec);
    },
    cancel() {
      this.show = false;
      this.$emit('cancel');
    },
    confirm() {
      const data = {
        userId: this.user.id,
        propId: this.prop.id,
        quantity: this.num
      };

      ReservationController.reservate(this.prop.id, data)
        .then(() => {
          this.prop.quantity -= this.num;
          this.$alert.success('Your reservation was successful');
          this.$emit('confirm', this.num);
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
