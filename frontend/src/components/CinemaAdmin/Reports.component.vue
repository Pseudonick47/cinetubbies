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
      <v-card width="40%">
        <v-card-text>Movies:</v-card-text>
        <v-expansion-panel>
          <v-expansion-panel-content
            v-for="movie in movies"
            :key="movie.id">
            <div slot="header">{{ movie.title }}</div>
            <v-card>
              <v-card-text>
                Genre: {{ movie.genre }} <br>
                Director: <span v-if="movie.director === ''">/</span><span v-else>{{ movie.director }}</span><br>
                Actors: <span v-if="movie.actors === ''">/</span><span v-else>{{ movie.actors }}</span><br>
                Duration: <span v-if="movie.duration === ''">/</span><span v-else>{{ movie.duration }}min</span><br>
                Description: <span v-if="movie.description === ''">/</span><span v-else>{{ movie.description }}</span><br>
                Average rating: <span v-if="movie.rating === null">/</span><span v-else>{{ movie.rating }}</span><br>
                Number of votes: {{ movie.voters_count }} <br>
              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
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
    theater: new Theater(),
    movies: [],
    num: 1
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
          TheaterController.getMovies(this.theater.id)
            .then((response) => {
              this.movies = response.data;
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
