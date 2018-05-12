<template>
  <v-layout column>
    <v-layout row>
      <v-flex
        s12
        sm5
        md9/>
      <v-flex
        s12
        sm5
        md4>
        <v-chip
          v-if="theater.kind==='m'"
          label
          outline
          color="white"
          center>
          Cinema revenue
        </v-chip>
        <v-chip
          v-else
          label
          outline
          color="white"
        >
          <v-icon>
            attach_money
          </v-icon>
          Theater revenue
        </v-chip>
        <v-divider/>
        <v-radio-group
          v-model="revenue"
          row>
          <v-radio
            label="Last week"
            value="week" />
          <v-radio
            label="Last month"
            value="month"/>
        </v-radio-group>
        <v-radio-group
          v-model="revenue"
          row>
          <v-radio
            label="Last year"
            value="year"/>
          <v-radio
            label="Overall"
            value="overall"/>
        </v-radio-group>
        <hr>
        <v-card-text v-if="revenue == null">
          Select the period for which you want to see the report
        </v-card-text>
      </v-flex>
    </v-layout>
    <hr>
    <v-layout row>
      <v-flex
        s12
        sm5
        md7>
        <v-layout column>
          <v-flex>
            <v-icon
              size="150px">
              star
            </v-icon>
          </v-flex>
          <v-flex>Average rating: {{ theater.rating }}</v-flex>
        </v-layout>
      </v-flex>
      <v-flex
        s12
        sm5
        md7>
        <v-layout column>
          <v-flex>
            <v-icon size="150px">
              people
            </v-icon>
          </v-flex>
          <v-flex>Number of ratings: {{ theater.voters_count }}</v-flex>
        </v-layout>
      </v-flex>
      <v-flex
        s12
        sm5
        md7>
        <v-layout column>
          <v-icon
            slot="activator"
            size="150px">
            movie
          </v-icon>
          <v-btn
            round
            @click="showMovieRatings = true">See movie ratings</v-btn>
        </v-layout>
        <v-dialog
          v-model="showMovieRatings"
          max-width="500px">
          <v-list three-line>
            <v-list-tile
              v-for="item in movies"
              :key="item.id"
            >
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                <v-list-tile-sub-title>
                  <v-icon>star</v-icon>
                  Averate rating: {{ item.rating }}
                </v-list-tile-sub-title>
                <v-list-tile-sub-title>
                  <v-icon>people</v-icon>
                  Number of ratings: {{ item.voters_count }}
                </v-list-tile-sub-title>
                <v-list-tile-sub-title><hr></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-dialog>
      </v-flex>
    </v-layout>
  </v-layout>
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
    revenue: null,
    showMovieRatings: false
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
