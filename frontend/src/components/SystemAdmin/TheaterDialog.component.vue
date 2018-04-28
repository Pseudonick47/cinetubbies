<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="500px"
  >
    <v-card>
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
          <v-radio-group
            v-validate="'required'"
            v-model="theater.kind"
            row
          >
            <v-radio
              label="Cinema"
              value="m"
            />
            <v-radio
              label="Theater"
              value="p"
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
          color="blue darken-1"
          flat
          @click.native="reset"
        >Close</v-btn>
        <v-btn
          color="blue darken-1"
          flat
          @click.native="submit"
        >Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import SystemAdminController from 'Controllers/system-admin.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'TheaterDialog',
  data() {
    return {
      show: true,
      theater: {
        name: '',
        address: '',
        kind: 'cinema'
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
