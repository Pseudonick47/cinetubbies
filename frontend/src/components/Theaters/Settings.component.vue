<template>
  <v-flex
    xs-12
    sm5
  >
    <v-chip
      color="white"
      text-color="black">
      <v-icon left>build</v-icon>
      Theater settings
    </v-chip>
    <v-chip
      color="white"
      text-color="black">
      <span v-if="theater.kind==='m'">Type: cinema</span>
      <span v-else>Type: theater</span>
      <v-tooltip right>
        <v-icon
          slot="activator"
          right
        >info</v-icon>
        <span>Types: cinema, theater</span>
      </v-tooltip>
    </v-chip>
    <form>
      <v-text-field
        v-model="theater.name"
        label="Name"
      />
      <v-text-field
        v-model="theater.address"
        label="Address"
      />
      <v-text-field
        v-model="theater.description"
        label="Description"
      />
      <v-btn @click="confirmSubmit = true">submit</v-btn>
    </form>
    <v-dialog
      v-model="confirmSubmit"
      persistent
      max-width="300px"
    >
      <v-card>
        <v-card-text>
          Submit changes?
        </v-card-text>
        <v-card-actions>
          <v-btn @click="submit">yes</v-btn>
          <v-spacer/>
          <v-btn @click="confirmSubmit = false">no</v-btn>
        </v-card-actions>

      </v-card>
    </v-dialog>
  </v-flex>
</template>

<script>
import TheatersController from 'Controllers/system-admin.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'TheaterSettings',

  data: () => ({
    loading: false,
    confirmSubmit: false,
    theater: {
      name: '',
      address: '',
      kind: '',
      description: ''
    }
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ])
  },
  mounted() {
    this.loadTheater();
  },
  methods: {
    loadTheater() {
      this.loading = true;
      TheatersController.get_theater(this.activeUser.id)
        .then((response) => {
          this.theater = response.data;
          this.loading = false;
        })
        .catch((response) => {
          this.loading = false;
          this.$alert.error('Error occurred.');
        });
    },
    submit() {
      this.confirmSubmit = false;
      let data = _.reduce(this.theater, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      this.$validator.validateAll().then((result) => {
        if (result) {
          TheatersController.update(data, this.activeUser.id).then((response) => {
            this.$alert.success('Settings successfully saved');
          }).catch(() => {
            this.$alert.error('Error while saving settings');
          });
          return;
        }
        this.$alert.error('Error while saving settings');
      });
    }
  }
};
</script>
