<template>
  <v-layout row>
    <v-flex
      s12
      sm5
      md6
      offset-lg
    >
      <v-list
        two-line
        subheader
      >
        <v-subheader>Cinemas</v-subheader>
        <v-list-tile>
          <v-text-field
            v-model="searchCinemas"
            append-icon="search"
            label="Search"
            class="mx-3"
          />
        </v-list-tile>
        <v-list-tile
          v-for="cinema in filteredCinemas"
          :key="cinema.id"
        >
          <v-list-tile-content>
            <v-list-tile-title>{{ cinema.name }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ cinema.description }}</v-list-tile-sub-title>
            <v-list-tile-sub-title><i>Location: {{ cinema.address }}</i></v-list-tile-sub-title>
            <v-list-tile-sub-title><i>Description: {{ cinema.description }}</i></v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon>{{ showStarIcon(cinema) }}</v-icon>
            <v-list-tile-action-text>{{ showTheaterRating(cinema) }}</v-list-tile-action-text>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>

    </v-flex>
    <v-flex
      s12
      sm5
      md6
      offset-lg1
    >
      <v-list
        two-line
        subheader
      >
        <v-subheader>Theaters</v-subheader>
        <v-list-tile>
          <v-text-field
            v-model="searchTheaters"
            append-icon="search"
            label="Search"
            class="mx-3"
          />
        </v-list-tile>
        <v-list-tile
          v-for="theater in filteredTheaters"
          :key="theater.id"
        >
          <v-list-tile-content>
            <v-list-tile-title>{{ theater.name }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ theater.description }}</v-list-tile-sub-title>
            <v-list-tile-sub-title><i>Location: {{ theater.address }}</i></v-list-tile-sub-title>
            <v-list-tile-sub-title><i>Description: {{ theater.description }}</i></v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon>{{ showStarIcon(theater) }}</v-icon>
            <v-list-tile-action-text>{{ showTheaterRating(theater) }}</v-list-tile-action-text>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>
</template>

<script>
import TheatersController from 'Controllers/system-admin.controller';
import { Theater } from 'Models/theater.model';

export default {
  name: 'Welcome',
  data: () => ({
    searchCinemas: '',
    searchTheaters: '',
    allTheaters: []
  }),
  computed: {
    filteredCinemas() {
      if (!_.isEmpty(this.searchCinemas)) {
        return this.allTheaters.filter((i) => {
          return i.isCinema() && i.name.toLowerCase().includes(_.trim(this.searchCinemas.toLowerCase()));
        });
      }
      return this.allTheaters.filter((i) => {
        return i.isCinema();
      });
    },
    filteredTheaters() {
      if (!_.isEmpty(this.searchTheaters)) {
        return this.allTheaters.filter((i) => {
          return i.isTheater() && i.name.toLowerCase().includes(_.trim(this.searchTheaters.toLowerCase()));
        });
      }
      return this.allTheaters.filter((i) => {
        return i.isTheater();
      });
    }
  },
  mounted() {
    this.getTheaters();
  },
  methods: {
    getTheaters() {
      TheatersController.getTheaters()
        .then((response) => {
          this.allTheaters = _.map(response.data, x => new Theater(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    showTheaterRating(theater) {
      if (theater.isRatingNull()) {
        return 'no rating';
      } else {
        return theater.rating + '/5';
      }
    },
    showStarIcon(theater) {
      if (theater.isRatingNull()) {
        return 'star_border';
      } else {
        return 'star';
      }
    }
  }
};
</script>
