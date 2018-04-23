<template>
  <v-app>
    <alert-box v-if="showAlert"/>
    <v-navigation-drawer
      v-model="drawer"
      fixed
      app>
      <v-list dense>
        <v-list-tile
          v-for="item in drawerItems[activeUserRole]"
          :key="item.title"
          :to="item.path">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>{{ item.text }}</v-list-tile-content>
        </v-list-tile>

        <template v-if="isAnyAdmin">
          <v-list-tile
            v-for="item in toolbarItems['admin']"
            :key="item.text"
            :to="item.path">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>{{ item.text }}</v-list-tile-content>
          </v-list-tile>
        </template>
        <v-list-tile
          v-if="isLogged"
          key="Logout"
          flat
          @click="logout">
          <v-list-tile-action>
            <v-icon>exit_to_app</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>Logout</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"/>
      <v-toolbar-title>Cinetubbies</v-toolbar-title>
      <v-spacer/>
      <v-toolbar-items class="hidden-sm-and-down"/>
    </v-toolbar>
    <v-content
      class="pt-2"
    >
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-content>
    <v-footer app/>
  </v-app>
</template>

<script>
import AlertBox from 'Components/helpers/AlertHelper.component';

import AuthController from 'Controllers/auth.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'App',
  components: {
    'alert-box': AlertBox
  },
  data() {
    return {
      drawer: false,
      toolbarItems: {
        'cinema_admin': [
          { icon: 'lock', text: 'Home', path: '/home' },
          { icon: 'add', text: 'New movie', path: '/movies/new' }
        ]
      },
      drawerItems: {
        'admin': [
          { icon: 'domain', text: 'Home', path: '/home' },
          { icon: 'theaters', text: 'Theaters', path: '/admin/theaters' },
          { icon: 'group', text: 'Cinema Admins', path: '/admin/cinema' },
          { icon: 'group', text: 'Fan Zone Admins', path: '/admin/fan-zone' }
        ],
        'cinema_admin': [
          { icon: 'person_add', text: 'Home', path: '/home' },
          { icon: 'add', text: 'New movie', path: '/movies/new' }
        ],
        'fan_zone_admin': [
          { icon: 'person_add', text: 'Home', path: '/home' }
        ],
        'user': [
          { icon: 'person_add', text: 'Home', path: '/home' },
          { icon: 'settings', text: 'Settings', path: '/user/settings' }
        ],
        'guest': [
          { icon: 'person_add', text: 'Login', path: '/login' },
          { icon: 'person_add', text: 'Register', path: '/register' }
        ]
      }
    };
  },
  computed: {
    ...mapGetters([
      'activeUser',
      'isAnyAdmin',
      'isAdmin',
      'isCinemaAdmin',
      'isFanZoneAdmin',
      'isLogged',
      'activeUserRole',
      'showAlert'
    ])
  },
  methods: {
    logout() {
      AuthController.logout();
    }
  }
};
</script>
<style>
  #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  /* color: #2c3e50; */
  margin-top: 60px;
}
</style>
