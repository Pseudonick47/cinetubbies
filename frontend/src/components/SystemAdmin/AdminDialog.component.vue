<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="500px"
  >
    <v-card color="black">
      <v-card-title>
        <span class="headline">Register New Admin</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-validate="'required|min:5'"
            v-model="admin.username"
            :error-messages="errors.collect('username')"
            prepend-icon="person"
            name="username"
            label="Username"
            type="text"
            data-vv-name="username"
            required
          />
          <v-text-field
            v-validate="'required|email'"
            v-model="admin.email"
            :error-messages="errors.collect('email')"
            prepend-icon="person"
            label="Email"
            type="email"
            data-vv-name="email"
            required
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
import SystemAdminController from 'Controllers/system-admin.controller';

export default {
  name: 'AdminDialog',
  props: {
    kind: {
      type: String,
      required: true
    },
    role: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      show: true,
      admin: {
        username: '',
        email: ''
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
          const admin = this.admin;
          admin.role = this.role;
          SystemAdminController.registerAdmin(admin, this.kind);
          this.close();
          return;
        }
        this.$alert.error('Please fill all required fields');
      });
    }
  }
};
</script>
