<template>
  <v-dialog
    v-model="show"
    max-width="600px"
    persistent
  >
    <v-card class="elevation-12">
      <v-toolbar
        dark
        color="primary">
        <v-toolbar-title>Find Friends</v-toolbar-title>
        <v-spacer/>
        <v-btn
          color="accent"
          @click="close"
        >Done
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <v-card>
          <v-card-title>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              autofocus
              hide-details
            />
          </v-card-title>
          <v-data-table
            :items="users"
            :total-items="users.length"
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
              <td>{{ props.item.first_name + props.item.last_name }}</td>
              <td class="text-xs-right">{{ props.item.city }}</td>
              <td class="justify-center layout px-0">
                <v-btn
                  icon
                  class="mx-0"
                  @click="addFriend(props.item.id)">
                  <v-icon color="teal">add_circle_outline</v-icon>
                </v-btn>
              </td>
            </template>
          </v-data-table>
        </v-card>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { User } from 'Models/user.model';
import UsersController from 'Controllers/users.controller';

export default {
  name: 'AddFriendModal',
  props: {
    show: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    search: '',
    pagination: {},
    users: []
  }),
  watch: {
    search(newVal, oldVal) {
      if (!_.isEmpty(newVal)) {
        this.searchFriends(newVal);
      }
    }
  },
  methods: {
    searchFriends(query) {
      UsersController.searchFriends(query).then((response) => {
        this.users = _.map(response.data.results, result => new User(result));
        this.$forceUpdate();
      });
    },
    addFriend(id) {
      const index = _.findIndex(this.users, { id });
      if (index > -1) {
        this.users.splice(index, 1);
      }
      this.$emit('add-friend', id);
    },
    close() {
      this.$emit('closed');
    }
  }
};
</script>
