<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="600px">
    <v-card class="elevation-12">
      <v-toolbar
        dark
        color="primary">
        <v-toolbar-title>Find Friends</v-toolbar-title>
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
            :items="friends"
            :total-items="friends.length"
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
                  @click="deleteItem(props.item)">
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
      }, {
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
      }, {
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
      }, {
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
      }, {
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
      }, {
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
  })
};
</script>
