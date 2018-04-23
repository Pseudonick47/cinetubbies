<template>
  <v-layout
    align-center
    justify-center>
    <v-flex
      xs12
      sm8
      md4>
      <v-card class="elevation-12">
        <v-toolbar
          dark
          color="primary">
          <v-toolbar-title>Register</v-toolbar-title>
        </v-toolbar>

        <v-card-text>
          <v-form>
            <v-text-field
              v-validate="'required|min:5'"
              v-model="formData.username"
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
              v-model="formData.email"
              :error-messages="errors.collect('email')"
              prepend-icon="person"
              label="Email"
              type="email"
              data-vv-name="email"
              required
            />
            <v-text-field
              v-validate="'required|min:5'"
              v-model="formData.password"
              :error-messages="errors.collect('password')"
              prepend-icon="lock"
              name="password"
              label="Password"
              type="password"
              data-vv-name="password"
              required
            />
            <v-text-field
              v-validate="'required|confirmed:password'"
              v-model="formData.password_confirm"
              :error-messages="errors.collect('password confirm')"
              prepend-icon="lock_outline"
              label="Confirm Password"
              type="password"
              data-vv-name="password confirm"
              required
            />
            <v-text-field
              v-validate="'required'"
              v-model="formData.first_name"
              :error-messages="errors.collect('first name')"
              prepend-icon="person"
              name="firstname"
              label="First Name"
              type="text"
              data-vv-name="first name"
              required
            />
            <v-text-field
              v-validate="'required'"
              v-model="formData.last_name"
              :error-messages="errors.collect('last name')"
              prepend-icon="person"
              name="lastname"
              label="Last Name"
              type="text"
              data-vv-name="last name"
              required
            />
            <v-text-field
              v-validate="'required'"
              v-model="formData.city"
              :error-messages="errors.collect('city')"
              prepend-icon="location_city"
              name="city"
              label="City"
              type="text"
              data-vv-name="city"
              required
            />
            <v-text-field
              v-validate="'required'"
              v-model="formData.phone"
              :error-messages="errors.collect('phone')"
              prepend-icon="phone"
              name="phone"
              label="Phone"
              type="text"
              data-vv-name="phone"
              required
            />
            <p
              v-for="(error, index) in formData.registerErrors"
              :key="index"
              class="register-errors"
            >
              {{ error }}
            </p>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="primary"
            @click="submit"
          >
            Register
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthController from 'Controllers/auth.controller';

export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        password: '',
        last_name: '',
        first_name: '',
        password_confirm: '',
        email: '',
        city: '',
        phone: '',
        registerErrors: []
      }
    };
  },
  methods: {
    submit() {
      this.$validator.validateAll().then((result) => {
        if (result) {
          AuthController.register(this.formData).catch(() => {
            this.$alert.error('Username already taken');
          });
          return;
        }
        this.$alert.error('Check fields!');
      });
    }
  }
};
</script>

<style>
.register-errors {
  color: red;
}
</style>
