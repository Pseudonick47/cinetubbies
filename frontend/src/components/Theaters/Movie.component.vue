<template>
  <div>
    <v-parallax
      src="http://blog.hdwallsource.com/wp-content/uploads/2017/05/fast-and-furious-8-logo-wallpaper-61267-63082-hd-wallpapers.jpg"
      class="paralax-kill-margins"
    >
      <v-layout
        column
        align-center
        justify-center>
        <h1 class="white--text title-text-shadow">{{ movie.title }}</h1>
        <h4 class="white--text title-text-shadow">by <i>{{ movie.director }}</i></h4>
      </v-layout>
    </v-parallax>
    <v-layout
      row
      class="my-3"
    >
      <v-flex md5>
        <h3>Title:{{ movie.title }}</h3>
        <h3>Director: {{ movie.director }}</h3>
        <h3>Genre: {{ movie.genre }}</h3>
        <h3>Duration: {{ movie.duration }}</h3>
        <h3>Actors: {{ movie.actors }}</h3>
        <h3>Description: {{ movie.description }}</h3>
        <h3>Rating: {{ movie.rating }}</h3>
      </v-flex>

      <v-flex md3>
        <v-date-picker
          v-model="selectedDate"
          :events="showtimeDates"
          full-width
          class="mx-3"
        />
      </v-flex>
      <v-flex md4>
        <v-data-table
          :items="selectedDateShowtimes"
          :total-items="showtimes.length"
          hide-headers
          hide-actions
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ props.item.auditorium }}</td>
            <td class="text-xs-right">{{ props.item.price }}</td>
            <td class="text-xs-right">{{ props.item.time }}</td>
            <td class="text-xs-right">{{ props.item.date }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                icon
                class="mx-0"
                @click="addFriend(props.item.id)">
                <v-icon color="teal">weekend</v-icon>
              </v-btn>
            </td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import * as _ from 'lodash';
import MovieController from 'Controllers/movies.controller';
import { Movie } from 'Models/movie.model';

export default {
  name: 'Movie',
  props: {
    theaterId: {
      type: String,
      required: true
    },
    movieId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedDate: null,
      movie: {},
      showtimes: []
    };
  },
  computed: {
    selectedDateShowtimes() {
      return _.filter(this.showtimes, { date: this.selectedDate });
    },
    showtimeDates() {
      return _.map(this.showtimes, (showtime) => {
        return showtime.date;
      });
    }
  },
  mounted() {
    this.getMovie(this.movieId);
    this.getShowtimes(this.movieId);
  },
  methods: {
    getMovie(id) {
      MovieController.retrieve(id)
        .then((response) => {
          this.movie = new Movie(response.data);
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getShowtimes(id) {
      MovieController.getShowtimes(id)
        .then((response) => {
          this.showtimes = response.data;
        })
        .catch(() => {
          this.$alert.error('Error occurred.');
        });
    }
  }
};
</script>

<style>
.title-text-shadow {
    text-shadow: 2px 2px 3px #555;
}

.paralax-kill-margins {
  margin-top: -20px;
  margin-left: -16px;
  margin-right: -16px;
}
</style>
