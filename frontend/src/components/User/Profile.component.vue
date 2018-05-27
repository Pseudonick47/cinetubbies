<template>
  <v-layout
    row
    wrap
    pa-4>
    <v-flex xs7>
      <v-card color="black">
        <v-card-title>
          <v-layout
            row
            wrap
            align-center>
            <div class="title">Bookings</div>
            <!-- <v-spacer/>
            <v-text-field
              v-model="searchBookings"
              append-icon="search"
              label="Search"
              single-line
              hide-details
              style="position: relative; top: -10px;"
            /> -->
          </v-layout>
        </v-card-title>
        <v-data-table
          v-if="bookings.length"
          :items="bookings"
          hide-headers
          hide-actions
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <!-- <td>
              <v-flex
                xs4
                sm2
                md1>
                <v-avatar
                  slot="activator"
                  size="36px"
                >
                  <img
                    src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460"
                    alt=""
                  >
                </v-avatar>
              </v-flex>
            </td> -->
            <td>{{ `${props.item.id}` }}</td>
            <td>{{ `seat: ${props.item.seat}` }}</td>
            <td class="text-xs-right">{{ props.item.showtime.time }}</td>
            <td class="text-xs-right">{{ props.item.showtime.price }}</td>
            <td class="text-xs-right">{{ `${props.item.discount} %` }}</td>
            <!-- <td class="justify-center layout px-0">
              <v-btn
                icon
                class="mx-0"
                @click="removeBooking(props.item.id)">
                <v-icon color="pink">remove_circle_outline</v-icon>
              </v-btn>
            </td> -->
          </template>
        </v-data-table>
      </v-card>
    </v-flex>
    <v-flex
      xs4
      offset-xs1
    >
      <v-card color="black">
        <v-card-title>
          <v-layout
            row
            wrap
            align-center>
            <div class="title">Friends</div>
            <v-btn
              icon
              class="mx-3"
              @click="showAddFriend = true"
            >
              <v-icon color="teal">add_circle_outline</v-icon>
            </v-btn>
            <v-spacer/>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
              style="position: relative; top: -10px;"
            />
          </v-layout>
        </v-card-title>
        <v-data-table
          v-if="friends.length"
          :items="friends"
          hide-headers
          hide-actions
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>
              <v-flex
                xs4
                sm2
                md1>
                <v-avatar
                  slot="activator"
                  size="36px"
                >
                  <img
                    src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460"
                    alt=""
                  >
                </v-avatar>
              </v-flex>
            </td>
            <td>{{ `${props.item.first_name} ${props.item.last_name}` }}</td>
            <td class="text-xs-right">{{ props.item.city }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                icon
                class="mx-0"
                @click="removeFriend(props.item.id)">
                <v-icon color="pink">remove_circle_outline</v-icon>
              </v-btn>
            </td>
          </template>
        </v-data-table>
        <template v-if="friendRequests.length">
          <hr>
          <hr>
          <br>
          <hr>
          <hr>
          <v-data-table
            :items="friendRequests"
            hide-headers
            hide-actions
            item-key="date"
            class="elevation-1"
          >
            <template
              slot="items"
              slot-scope="props">
              <td>
                <v-flex
                  xs4
                  sm2
                  md1>
                  <v-avatar
                    slot="activator"
                    size="36px"
                  >
                    <img
                      src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460"
                      alt=""
                    >
                  </v-avatar>
                </v-flex>
              </td>
              <td>{{ `${props.item.first_name} ${props.item.last_name}` }}</td>
              <td class="text-xs-right">{{ props.item.city }}</td>
              <td class="justify-center layout px-0">
                <v-btn
                  icon
                  class="mx-0"
                  @click="addFriend(props.item.id)">
                  <v-icon color="teal">check</v-icon>
                </v-btn>
                <v-btn
                  icon
                  class="mx-0"
                  @click="declineRequest(props.item.id)">
                  <v-icon color="pink">clear</v-icon>
                </v-btn>
              </td>
            </template>
          </v-data-table>
        </template>
      </v-card>
    </v-flex>
    <add-friend-modal
      v-if="showAddFriend"
      @add-friend="addFriend"
      @closed="showAddFriend = false"
    />
  </v-layout>
</template>

<script>
import AddFriendModal from 'Components/User/AddFriendModal.component';
import UsersController from 'Controllers/users.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'UserSettings',
  components: {
    AddFriendModal
  },
  data: () => ({
    showAddFriend: false,
    bookings: [],
    search: '',
    users: [],
    pagination: {},
    allFriends: [],
    allFriendRequests: []
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ]),
    friendRequests() {
      return this.searchUsersByFirstOrLastName(this.allFriendRequests, this.search);
    },
    friends() {
      return this.searchUsersByFirstOrLastName(this.allFriends, this.search);
    }
  },
  created() {
    UsersController.getProfile(this.activeUser.id).then((response) => {
      this.allFriends = response.data.friends;
      this.allFriendRequests = response.data.friend_requests;
      this.bookings = response.data.bookings;
    });
  },
  methods: {
    searchUsersByFirstOrLastName(userList, name) {
      if (!name) {
        return userList;
      }
      return _.filter(userList, user =>
        _.toLower(user.first_name).indexOf(_.toLower(name)) > -1 || _.toLower(user.last_name).indexOf(_.toLower(name)) > -1);
    },
    declineRequest(id) {
      UsersController.removeFriend(id).then(() => {
        const index = _.findIndex(this.allFriendRequests, { id });
        if (index > -1) {
          this.allFriendRequests.splice(index, 1);
        }
      }).catch(() => {
        this.$alert.error('Error occured while declining friendship');
      });
    },
    removeFriend(id) {
      UsersController.removeFriend(id).then((response) => {
        const index = _.findIndex(this.allFriends, { id });
        if (index > -1) {
          this.allFriends.splice(index, 1);
        }
      }).catch(() => {
        this.$alert.error('Error occured while removing friend');
      });
    },
    addFriend(id) {
      UsersController.addFriend(id).then(() => {
        const index = _.findIndex(this.allFriendRequests, { id });
        if (index > -1) {
          let added = _.remove(this.allFriendRequests, { id });
          this.allFriends.push(added[0]);
        }
      });
    }
  }
};
</script>
