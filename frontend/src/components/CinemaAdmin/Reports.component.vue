<template>
  <div>
    Hello. You are admin for this theater.<br><br>
    <v-flex>
      <v-card width="40%">
        <v-card-text>Name: {{ theater.name }}</v-card-text>
      </v-card>
      <v-card width="40%">
        <v-card-text>Address: {{ theater.address }}</v-card-text>
      </v-card>
      <v-card width="40%">
        <v-card-text>Description: {{ theater.description }}</v-card-text>
      </v-card>
      <v-card width="40%">
        <v-card-text>Average rating:
          <span v-if="theater.rating === null">Rating is not available at the moment.</span>
          <span v-else>{{ theater.rating }}</span>
        </v-card-text>
      </v-card>
      <v-card width="40%">
        <v-card-text>Number of voters: {{ theater.voters_count }}</v-card-text>
      </v-card>
  </v-flex></div>
</template>

<script>
import { mapGetters } from 'vuex';
import { Theater } from 'Models/theater.model';
import TheaterController from 'Controllers/system-admin.controller';

export default {
  name: 'Reports',
  data: () => ({
    theater: new Theater()
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ])
  },
  mounted() {
    this.getTheater();
  },
  methods: {
    getTheater() {
      TheaterController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theater = new Theater(response.data);
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
