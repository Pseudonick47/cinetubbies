<template>
  <v-dialog
    v-model="showThis"
    width="800px"
    persistent
    color="secondary"
    lazy
  >
    <!-- <v-btn
      slot="activator"
      color="primary"
    >
      Open Dialog
    </v-btn> -->
    <v-card>
      <v-card-title>
        <span class="headline">Choose seat to finish booking</span>
      </v-card-title>
      <v-card-text>
        <v-card-text>
          <layout
            :seats.sync="layout"
          />

        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="error darken-1"
            flat
            @click.native="cancel">Cancel</v-btn>
          <v-btn
            color="info darken-1"
            @click.native="bookTicket">
            book
            <v-icon class="ml-2">send</v-icon>
          </v-btn>
        </v-card-actions>
    </v-card-text></v-card>
  </v-dialog>
</template>
<script>
import Layout from 'Components/Auditorium/Layout.component';
export default {
  name: 'BookTicketDialog',
  components: {
    Layout
  },
  props: {
    show: {
      type: Boolean,
      required: true
    },
    showtimeId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      selectedSeats: [ 1, 2, 44 ],
      layout: [
        [ 0, 1, 0, 1 ],
        [ 1, 0, 0, 1 ],
        [ 1, 1, 1, 1 ]
      ]
    };
  },
  computed: {
    showThis: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit('update:show', value);
      }
    }
  },
  methods: {
    bookTicket() {
      this.$emit('book-ticket', this.selectedSeats);
    },
    cancel() {
      this.$emit('cancel');
    }
  }
};
</script>
<style>
.seats-mockup {
  height: 200px;
  width: 400px;
  margin: auto;
  background: rgb(123, 123, 123);
}
</style>
