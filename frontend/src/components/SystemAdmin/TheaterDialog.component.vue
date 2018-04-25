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
            v-model="theater.name"
            :error-messages="errors.collect('name')"
            prepend-icon="person"
            name="name"
            label="Name"
            type="text"
            required
          />
          <v-text-field
            v-model="theater.address"
            :error-messages="errors.collect('address')"
            prepend-icon="person"
            name="address"
            label="Address"
            type="text"
            required
          />
          <v-select
            v-model="theater.kind"
            :items="['Cinema', 'Theater']"
            label="Kind"
            required
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

const MAP_KIND = {
  'Cinema': 'm',
  'Theater': 'p'
};

export default {
  name: 'TheaterDialog',
  data() {
    return {
      show: true,
      theater: {
        name: '',
        address: '',
        kind: 'Cinema'
      }
    };
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
          theater.kind = MAP_KIND[theater.kind];
          // TODO: select an admin
          theater.admin_id = 2;
          SystemAdminController.registerTheater(theater);
          this.close();
          return;
        }
        this.$alert.error('Please fill all required fields');
      });
    }
  }
};
</script>
