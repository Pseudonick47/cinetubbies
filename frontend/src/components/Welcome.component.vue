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
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon
              v-if="cinema.rating == null"
            >star_border</v-icon>
            <v-icon
              v-else
            >star</v-icon>
            <v-list-tile-action-text v-if="cinema.rating == null">no rating</v-list-tile-action-text>
            <v-list-tile-action-text v-else>{{ cinema.rating }}/5</v-list-tile-action-text>
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
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon
              v-if="theater.rating == null"
            >star_border</v-icon>
            <v-icon
              v-else
            >star</v-icon>
            <v-list-tile-action-text v-if="theater.rating == null">no rating</v-list-tile-action-text>
            <v-list-tile-action-text v-else>{{ theater.rating }}/5</v-list-tile-action-text>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>
</template>

<script>
import TheatersController from 'Controllers/system-admin.controller';

export default {
  name: 'Welcome',
  data: () => ({
    searchCinemas: '',
    searchTheaters: '',
    all: []
  }),
  computed: {
    filteredCinemas() {
      if (!_.isEmpty(this.searchCinemas)) {
        return this.all.filter((i) => {
          return i.kind === 'm' && i.name.toLowerCase().includes(_.trim(this.searchCinemas.toLowerCase()));
        });
      }
      return this.all.filter((i) => {
        return i.kind === 'm';
      });
    },
    filteredTheaters() {
      if (!_.isEmpty(this.searchTheaters)) {
        return this.all.filter((i) => {
          return i.kind === 'p' && i.name.toLowerCase().includes(_.trim(this.searchTheaters.toLowerCase()));
        });
      }
      return this.all.filter((i) => {
        return i.kind === 'p';
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
          this.all = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
