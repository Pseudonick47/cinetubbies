<template>
  <v-layout
    row
    wrap>
    <v-flex
      xs4
      offset-xs8>
      <v-card>
        <v-card-title>
          Friends
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
          />
        </v-card-title>
        <v-data-table
          :items="friends"
          :pagination.sync="pagination"
          :rows-per-page-items="[5, 10, 20, 50, 100]"
          hide-headers
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
            <td>{{ props.item.first_name + props.item.last_name }}</td>
            <td class="text-xs-right">{{ props.item.city }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                icon
                class="mx-0"
                @click="editItem(props.item)">
                <v-icon color="teal">call_made</v-icon>
              </v-btn>
              <v-btn
                icon
                class="mx-0"
                @click="deleteItem(props.item)">
                <v-icon color="pink">remove_circle_outline</v-icon>
              </v-btn>
            </td>
          </template>
        </v-data-table>
      </v-card>
    </v-flex>
    <add-friend-modal v-if="showAddFriend"/>
  </v-layout>
</template>

<script>
import AddFriendModal from 'Components/User/AddFriendModal.component';
import UsersController from 'Controllers/users.controller';
import { mapGetters } from 'vuex';

var moment = require('moment');

export default {
  name: 'UserSettings',
  components: {
    AddFriendModal
  },
  data: () => ({
    showAddFriend: true,
    search: '',
    pagination: {},
    friends: [
      {
        first_name: 'Ime',
        last_name: 'Prezime',
        city: 'Novi Sad'
      },
      {
        first_name: 'Ime',
        last_name: 'Prezime',
        city: 'Novi Sad'
      },
      {
        first_name: 'Ime',
        last_name: 'Prezime',
        city: 'Novi Sad'
      }
    ]
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ])
  },
  methods: {

  }
};
</script>
