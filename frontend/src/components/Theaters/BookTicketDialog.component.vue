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
        <span class="headline"> {{ isInvitingFriends ? 'Select friends to invite' : 'Choose seat to finish booking' }}</span>
      </v-card-title>
      <v-card-text>
        <v-card-text>
          <template v-if="!isInvitingFriends">
            <layout
              :seats.sync="layout"
              :last-selected.sync="selectedSeats"
            />
          </template>
          <template v-else>
            <v-select
              v-model="selectedFriends"
              :items="allFriends"
              item-text="first_name"
              item-value="id"
              label="Select friends"
              multiple
              max-height="400"
              hint="Pick friends you would like to invite"
              persistent-hint
            />
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="error darken-1"
            flat
            @click.native="cancel">Cancel</v-btn>
          <v-btn
            v-if="!isInvitingFriends"
            color="info darken-1"
            @click.native="bookTicket">
            book
            <v-icon class="ml-2">send</v-icon>
          </v-btn>
          <v-btn
            v-else
            color="info darken-1"
            @click.native="inviteFriends">
            invite
            <v-icon class="ml-2">email</v-icon>
          </v-btn>
        </v-card-actions>
    </v-card-text></v-card>
  </v-dialog>
</template>
<script>
import Layout from 'Components/Auditorium/Layout.component';
import UsersController from 'Controllers/users.controller';
import { mapGetters } from 'vuex';

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
      isInvitingFriends: false,
      allFriends: [],
      selectedFriends: [],
      selectedSeats: []
    };
  },
  computed: {
    ...mapGetters([
      'activeUser'
    ]),
    layout() {
      const showtime = this.showtime(this.showtimeId);
      const auditorium = this.auditorium(showtime.auditorium);
      const size = auditorium.layout[0].length;
      let chunked = _.chunk(this.showtimeSeats(this.showtimeId), size);
      return chunked;
    },
    ...mapGetters([ 'showtimeSeats', 'showtime', 'auditorium' ]),
    showThis: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit('update:show', value);
      }
    }
  },
  created() {
    UsersController.getProfile(this.activeUser.id).then((response) => {
      this.allFriends = response.data.friends;
    });
  },
  methods: {
    bookTicket() {
      let mayInviteFriends = !!(this.selectedSeats.length - 1);
      // [ {x:1, y:4}]
      this.$emit('book-ticket', this.selectedSeats, mayInviteFriends);
      this.isInvitingFriends = !!this.selectedSeats.length;
    },
    cancel() {
      this.$emit('cancel');
    },
    inviteFriends() {
      // [ { user: id, seat: id }... ]
      this.$emit('invite-friends', this.selectedFriends, this.selectedSeats); // [ {x:1, y:4}]
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
