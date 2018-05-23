<template>
  <v-card
    class="theater-card"
    color="black"
  >
    <v-card-media
      src="http://arab-culture.info/wp-content/uploads/2018/02/1-68.jpg"
      height="200px"
    />
    <v-card-title primary-title>
      <v-layout
        row
        justify-space-between
      >
        <v-flex>
          <div>
            <div class="headline">{{ info.name }}</div>
            <span class="grey--text">{{ info.address }}</span>
          </div>
        </v-flex>
        <!-- <v-flex
          xs2
          justify-end
        >
          <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-width="200"
            offset-x
          >
            <v-btn
              slot="activator"
              class="elevation-1"
              fab
              dark
              small
              color="primary"
            >
              <v-icon dark>account_circle</v-icon>
            </v-btn>
            <v-card>
              <v-card-title primary-title>
                <div>
                  <div class="headline">{{ admin.username }}</div>
                  <span class="grey--text">{{ admin.email }}</span>
                </div>
              </v-card-title>
            </v-card>
          </v-menu>
        </v-flex> -->
      </v-layout>
    </v-card-title>
    <v-card-text>
      I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
    </v-card-text>
    <v-card-actions>
      <v-layout
        row
        justify-space-between
      >
        <v-btn
          flat
          color="primary"
          @click="edit"
        >
          Edit
        </v-btn>
        <v-btn
          flat
          color="primary"
          @click="remove"
        >
          Remove
        </v-btn>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Theater',
  props: {
    info: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      menu: false
    };
  },
  computed: {
    admin() {
      const a = this.$store.getters['systemAdmin/theaterAdmin'](this.info.admin_id);
      return a || { username: '', email: '' };
    }
  },
  methods: {
    edit() {
      this.$emit('editTheater', this.info.id);
    },
    remove() {
      this.$emit('removeTheater', this.info.id);
    }
  }
};
</script>

<style>

.theater-card {
  height: 100% !important;
  justify-content: space-between;
  flex-direction: column;
  display: flex;
}

</style>
