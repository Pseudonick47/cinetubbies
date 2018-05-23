<template>
  <v-app
    dark
    fill-height
  >
    <alert-box v-if="showAlert"/>
    <v-navigation-drawer
      v-model="drawer"
      class="my-drawer pl-2 pt-4"
      fixed
      left
      floating
      app
    >
      <v-list>
        <template
          v-for="item in drawerItems[activeUserRole]"
        >
          <v-list-group
            v-if="item.children"
            :key="item.title"
          >
            <v-list-tile slot="activator">
              <v-list-tile-title class="title">{{ item.text }}</v-list-tile-title>
            </v-list-tile>
            <v-list-tile
              v-for="subitem in item.children"
              :key="subitem.title"
              :to="subitem.path"
            >
              <v-list-tile-content class="title pl-4">{{ subitem.text }}</v-list-tile-content>
            </v-list-tile>
          </v-list-group>
          <v-list-tile
            v-else
            :key="item.title"
            :to="item.path"
            class="item-tile"
          >
            <v-list-tile-content class="title">{{ item.text }}</v-list-tile-content>
          </v-list-tile>
        </template>
        <template v-if="isAnyAdmin">
          <v-list-tile
            v-for="item in toolbarItems['admin']"
            :key="item.text"
            :to="item.path">
            <!-- <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action> -->
            <v-list-tile-content class="title">{{ item.text }}</v-list-tile-content>
          </v-list-tile>
        </template>
        <v-list-tile
          v-if="isLogged"
          key="Logout"
          flat
          @click="logout">
          <!-- <v-list-tile-action>
            <v-icon>exit_to_app</v-icon>
          </v-list-tile-action> -->
          <v-list-tile-content class="title">Logout</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      app
      flat
      style="background-color: black"
    >
      <div class="toolbar-background">
        <v-layout
          class="toolbar-content"
          row
        >
          <v-toolbar-side-icon @click.stop="drawer = !drawer"/>
          <v-spacer/>
          <v-toolbar-title class="display-1">Cinetubbies</v-toolbar-title>
          <v-spacer/>
          <v-btn
            v-if="showRightDrawer"
            icon
            @click.stop="toggleRightDrawer"
          >
            <v-icon>more_vert</v-icon>
          </v-btn>
        </v-layout>
      </div>
    </v-toolbar>
    <v-content
      id="content"
      class="my-background pt-2 fill-height"
    >
      <v-container
        fill-height
        fluid
        pa-0
      >
        <router-view/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import AlertBox from 'Components/helpers/AlertHelper.component';

import AuthController from 'Controllers/auth.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'App',
  components: {
    'alert-box': AlertBox,
    'vue-datetime-picker': require('vue-datetime-picker')
  },
  data() {
    return {
      drawer: false,
      toolbarItems: {
        'cinema_admin': [
          { icon: 'lock', text: 'Home', path: '/home' }
        ]
      },
      drawerItems: {
        'admin': [
          { icon: 'home', text: 'Home', path: '/home' },
          { icon: 'theaters', text: 'Theaters/Cinemas', path: '/admin/system/theaters' },
          {
            icon: 'group',
            text: 'Admins',
            children: [
              { text: 'Theater/Cinema', path: '/admin/system/theater-admins' },
              { text: 'Fan Zone', path: '/admin/system/fan-zone-admins' },
              { text: 'System', path: '/admin/system/system-admins' }
            ]
          },
          { icon: 'star', text: 'Rewarding scale', path: '/admin/system/rewards' }
        ],
        'cinema_admin': [
          { icon: 'build', text: 'Theater', path: '/theater/settings' },
          { icon: 'edit', text: 'Theater shows', path: '/movies' },
          { icon: 'edit', text: 'Showtimes', path: '/showtimes' },
          { icon: 'edit', text: 'Tickets on sale', path: '/tickets-on-sale' },
          { icon: 'list', text: 'Reports', path: '/reports' },
          { icon: 'person', text: 'Account settings', path: '/user/settings' }
        ],
        'fan_zone_admin': [
          { icon: 'home', text: 'Home', path: '/home' },
          { icon: 'shopping_cart', text: 'Official Props', path: '/admin/fan-zone/home' },
          { icon: 'shopping_cart', text: 'Pending Props', path: '/admin/fan-zone/pending' }
        ],
        'user': [
          { icon: 'home', text: 'Home', path: '/home' },
          { icon: 'person_add', text: 'Profile', path: '/user/profile' },
          {
            icon: 'shopping_cart',
            text: 'Fan Zone',
            children: [
              { icon: 'shopping_cart', text: 'Shop', path: '/fan-zone' },
              { icon: 'shopping_cart', text: 'My Props', path: '/user/props' },
              { icon: 'shopping_cart', text: 'My Prop Reservations', path: '/user/prop-reservations' },
              { icon: 'shopping_cart', text: 'My Offers', path: '/user/prop-offers' }
            ]
          },
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
    ]),
    ...mapGetters('miscellaneous', {
      showRightDrawer: 'hasDrawer'
    })
  },
  methods: {
    logout() {
      AuthController.logout();
    },
    toggleRightDrawer() {
      this.$store.commit('miscellaneous/setDrawer', !this.$store.getters['miscellaneous/drawer']);
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
  min-height: calc(100vh - 60px);
}

#content {
  height: 100%;
}

.application--wrap {
  min-height: 0;
}

.content--wrap {
  padding: 0;
  height: 100%;
}

.my-background {
  background: linear-gradient(90deg, rgb(6,6,6), rgb(20,20,20), rgb(28,28,28), rgb(20,20,20), rgb(6,6,6));
  /* background-color: rgba(87, 71, 32, 0.87) */
}

.my-drawer {
  background-color: rgb(0,0,0) !important;
}

.toolbar-background {
  width: 100%;
  height: 100%;
  padding-bottom: 2px;
  background: linear-gradient(90deg, black, #c5951ba8, #a37b16, #c5951ba8,  black);
}

.toolbar-content {
  background:
    radial-gradient(ellipse at top, rgba(0, 0, 0, 0.7),rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)),
    linear-gradient(90deg, rgb(2,2,2), rgb(12,12,12), rgb(16,16,16), rgb(12,12,12), rgb(2,2,2));
  height: 100%;
  display: flex;
  align-items: center;
}

.item-tile:link {
  color: goldenrod;
}

</style>
