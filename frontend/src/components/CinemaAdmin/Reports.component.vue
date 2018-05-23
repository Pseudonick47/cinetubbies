<template>
  <v-layout column>
    <v-layout row>
      <v-flex
        s12
        sm5
        md9>
        <v-chip
          label
          outline
          color="white"
          center>
          <v-icon>
            people
          </v-icon>
          <span>&emsp;{{ theaterType }} attendance</span>
        </v-chip>
        <v-divider/>
        <v-radio-group
          v-model="chartPeriod"
          column
          @change="changeChartLabels()"
        >
          <v-radio
            label="This week"
            value="week"/>
          <v-radio
            label="This month"
            value="month"/>
          <v-radio
            label="This year"
            value="year"/>
          <v-radio
            label="Overall"
            value="overall"/>
        </v-radio-group>
        <v-container v-show="chartPeriod==='week'">
          <chart
            :data="datacollection"
            :height="160"
          />
        </v-container>
        <v-container v-show="chartPeriod==='month'">
          <chart
            :data="datacollection"
            :height="160"
          />
        </v-container>
        <v-container v-show="chartPeriod==='year'">
          <chart
            :data="datacollection"
            :height="160"
          />
        </v-container>
        <v-container v-show="chartPeriod==='overall'">
          <chart
            :data="datacollection"
            :height="160"
          />
        </v-container>
      </v-flex>
      <span>&emsp;&emsp;&emsp;&emsp;&emsp;</span>
      <v-flex
        s12
        sm5
        md4
      >
        <v-chip
          label
          outline
          color="white"
          center>
          <v-icon>
            attach_money
          </v-icon>
          {{ theaterType }} revenue
        </v-chip>
        <v-divider/>
        <v-radio-group
          v-model="type"
          row
          @change="changeType()"
        >
          <v-radio
            label="Date"
            value="date"/>
          <v-radio
            label="Month"
            value="month"/>
          <v-radio
            label="Year"
            value="year"/>
          <v-radio
            label="All"
            value="all"/>
        </v-radio-group>
        <v-flex v-show="pickDate">
          <v-menu
            ref="dateMenu1"
            :close-on-content-click="false"
            v-model="dateMenu1"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="date1"
              label="Start date"
              hint="YYYY-MM-DD format"
              persistent-hint
              prepend-icon="event"
              readonly
            />
            <v-date-picker
              v-model="date1"
              no-title
              @input="dateMenu1 = false"/>
          </v-menu>
          <v-menu
            :close-on-content-click="false"
            v-model="dateMenu2"
            :nudge-right="40"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"
          >
            <v-text-field
              slot="activator"
              v-model="date2"
              label="End date"
              hint="YYYY-MM-DD format"
              persistent-hint
              prepend-icon="event"
              readonly
            />
            <v-date-picker
              v-model="date2"
              :min="date1"
              no-title
              @input="dateMenu2 = false"/>
          </v-menu>
        </v-flex>
        <v-flex v-show="pickMonth">
          <v-date-picker
            v-model="month"
            type="month"/>
        </v-flex>
        <v-flex v-show="pickYear">
          <v-text-field
            slot="activator"
            v-model="year"
            label="Year"
            persistent-hint
            prepend-icon="event"
          />
        </v-flex>
        <v-btn @click="showRevenue()">ok</v-btn>
        <hr>
        <v-card-text>{{ revenue }}</v-card-text>
      </v-flex>
    </v-layout>
    <hr>
    <v-footer
      height="150"
    >
      <v-layout
        row>
        <v-flex
          s12
          sm5
          md7>
          <v-layout column>
            <v-flex>
              <v-icon
                size="100px">
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
              <v-icon size="100px">
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
              size="100px">
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
    </v-footer>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex';
import { Theater } from 'Models/theater.model';
import { Movie } from 'Models/movie.model';
import TheaterController from 'Controllers/system-admin.controller';
import Chart from 'Components/CinemaAdmin/Chart.component';

const REVENUE_MESSAGE = 'Select the period for which you want to see the report and click OK.';

export default {
  name: 'Reports',
  components: { 'chart': Chart },
  data: () => ({
    theater: new Theater(),
    movies: [],
    type: null,
    showMovieRatings: false,
    revenue: REVENUE_MESSAGE,
    date1: null,
    date2: null,
    month: null,
    year: null,
    dateMenu1: false,
    dateMenu2: false,
    pickDate: false,
    pickMonth: false,
    pickYear: false,
    chartPeriod: '',
    datacollection: { labels: [],
      datasets: [
        {
          label: 'Number of visitors',
          backgroundColor: '#6BAFB0',
          borderColor: '#2E8F91',
          hoverBackgroundColor: '#8ED2D3',
          borderWidth: 5,
          data: []
        }
      ] }
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'labelsWeek',
      'labelsMonth',
      'labelsYear',
      'labelsAll'
    ]),
    theaterType() {
      if (this.theater.isCinema()) {
        return 'Cinema';
      } else {
        return 'Theater';
      }
    }
  },
  mounted() {
    this.getTheater();
  },
  methods: {
    changeChartLabels() {
      if (this.chartPeriod === 'week') {
        this.datacollection.labels = this.labelsWeek;
      } else if (this.chartPeriod === 'month') {
        this.datacollection.labels = this.labelsMonth;
      } else if (this.chartPeriod === 'year') {
        this.datacollection.labels = this.labelsYear;
      } else {
        this.datacollection.labels = this.labelsAll;
      }
      TheaterController.getAttendance(this.theater.id, this.chartPeriod)
        .then((response) => {
          this.datacollection.datasets[0].data = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getTheater() {
      TheaterController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theater = new Theater(response.data);
          TheaterController.getMovies(this.theater.id)
            .then((response) => {
              this.movies = _.map(response.data, x => new Movie(x));
            })
            .catch((response) => {
              this.$alert.error('Error occurred.');
            });
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    showRevenue() {
      let data = { type: '', date1: '', date2: '', month: '', year: '' };
      data['type'] = this.type;
      data['date1'] = this.date1;
      data['date2'] = this.date2;
      data['month'] = this.month;
      data['year'] = this.year;
      TheaterController.getRevenue(this.theater.id, data)
        .then((response) => {
          this.revenue = response.data;
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    changeType() {
      if (this.type == 'date') {
        this.pickDate = true;
        this.pickMonth = false;
        this.pickYear = false;
      } else if (this.type == 'month') {
        this.pickDate = false;
        this.pickMonth = true;
        this.pickYear = false;
      } else if (this.type == 'year') {
        this.pickDate = false;
        this.pickMonth = false;
        this.pickYear = true;
      } else {
        this.pickDate = false;
        this.pickMonth = false;
        this.pickYear = false;
      }
      this.revenue = REVENUE_MESSAGE;
    }
  }
};
</script>
