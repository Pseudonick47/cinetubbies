<template>
  <v-layout row>
    <v-flex
      s12
      sm5
      md5
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
          :key="cinema.id" >
          <v-list-tile-content>
            <v-list-tile-title>{{ cinema.name }}, <i>{{ cinema.address }}<i/></i></v-list-tile-title>
            <v-list-tile-sub-title><i>rating: </i>{{ cinema.rating }}/5</v-list-tile-sub-title>
            <v-list-tile-sub-title><i>votes: </i> {{ cinema.voters_count }}
            <v-divider/></v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <star-rating
              v-model="cinema.all_votes[activeUser.id]"
              :max-rating="5"
              :star-size="20"
              inactive-color="#cc99ff"
              active-color="#9900cc"
              @rating-selected="setRating(cinema.id,$event)"
            />
          </v-list-tile-action>
        </v-list-tile>

      </v-list>

    </v-flex>
    <v-flex
      s12
      sm5
      md5
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
          :key="theater.id" >
          <v-list-tile-content>
            <v-list-tile-title>{{ theater.name }}, <i>{{ theater.address }}<i/></i></v-list-tile-title>
            <v-list-tile-sub-title><i>rating: </i>{{ theater.rating }}/5</v-list-tile-sub-title>
            <v-list-tile-sub-title><i>votes: </i>{{ theater.voters_count }}
            <v-divider/></v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <star-rating
              v-model="theater.all_votes[activeUser.id]"
              :max-rating="5"
              :star-size="20"
              inactive-color="#cc99ff"
              active-color="#9900cc"
              @rating-selected="setRating(theater.id,$event)"
            />
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>
</template>

<script>
import StarRating from 'vue-star-rating';
import TheatersController from 'Controllers/theaters.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'Home',
  components: {
    StarRating
  },
  data: () => ({
    loading: false,
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
    },
    ...mapGetters([
      'activeUser'
    ])
  },
  mounted() {
    this.getTheaters();
  },
  methods: {
    setRating(id, rating) {
      const data = { 'rating': rating, 'id': id };
      TheatersController.updateRating(data)
        .then((response) => {
          let found = this.all.find(function(element) {
            return element.id === id;
          });
          found['rating'] = response.data['rating']['rating'];
          found['voters_count'] = response.data['voters'];
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getTheaters() {
      this.loading = true;
      TheatersController.getTheaters()
        .then((response) => {
          this.all = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>
