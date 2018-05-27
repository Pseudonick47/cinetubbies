<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="500px"
  >
    <v-card color="black">
      <v-card-title>
        <span class="headline">Register New Theater</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-validate="'required'"
            v-model="theater.name"
            :error-messages="errors.collect('name')"
            prepend-icon="person"
            name="name"
            label="Name"
            type="text"
            required
          />
          <v-text-field
            v-validate="'required'"
            v-model="theater.address"
            :error-messages="errors.collect('address')"
            prepend-icon="person"
            name="address"
            label="Address"
            type="text"
            required
          />

          <v-expansion-panel>
            <v-expansion-panel-content>
              <div slot="header">Set location</div>
              <v-card>
                <g-map
                  :read-only="false"
                  @marker-updated="setMarker"
                />
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-radio-group
            v-validate="'required'"
            v-model="theater.kind"
            row
          >
            <v-radio
              label="Cinema"
              value="m"
              color="primary"
            />
            <v-radio
              label="Theater"
              value="p"
              color="primary"
            />
          </v-radio-group>
          <v-select
            v-validate="'required'"
            :items="admins"
            v-model="selected_admins"
            label="Admin"
            item-text="username"
            autocomplete
            return-object
            required
            multiple
          />
        </v-form>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          flat
          @click.native="reset"
        >Close</v-btn>
        <v-btn
          color="primary"
          flat
          @click.native="submit"
        >Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import GMap from 'Components/Map.component';
import SystemAdminController from 'Controllers/system-admin.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'TheaterDialog',
  components: {
    GMap
  },
  data() {
    return {
      show: true,
      theater: {
        name: '',
        address: '',
        lat: 0,
        lng: 0,
        kind: 'cinema',
        theateradmins: [],
        fanzoneadmins: []
      },
      selected_admins: null
    };
  },
  computed: {
    ...mapGetters('systemAdmin', {
      admins: 'theaterAdmins'
    })
  },
  methods: {
    setMarker(position) {
      this.theater.lat = position.lat;
      this.theater.lng = position.lng;
    },
    close() {
      this.show = false;
      this.$emit('close');
    },
    reset() {
      this.$refs.form.reset();
      this.close();
    },
    submit() {
      this.$validator.validateAll().then((result) => {
        if (result) {
          const theater = this.theater;
          theater.admins = _.map(this.selected_admins, 'id');

          SystemAdminController.registerTheater(theater)
            .then((response) => {
              SystemAdminController.requestCount('theaters');
              SystemAdminController.requestPage(this.$store.getters['systemAdmin/page'], 'theaters');
              this.$alert.success('Theater/cinema has been created!');
            })
            .catch(() => {
              this.$alert.error('Something went wrong. Please try again.');
            });

          this.close();
          return;
        }
        this.$alert.error('Please fill all required fields');
      });
    }
  }
};
</script>
