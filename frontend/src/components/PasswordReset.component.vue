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
          <v-toolbar-title>New password</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              v-validate="'required|min:5'"
              v-model="password"
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
              v-model="passwordConfirm"
              :error-messages="errors.collect('password confirm')"
              prepend-icon="lock_outline"
              label="Confirm Password"
              type="password"
              data-vv-name="password confirm"
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="primary"
            @click="confirm">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthController from 'Controllers/auth.controller';

export default {
  name: 'PasswordReset',
  props: {
    token: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      password: null,
      passwordConfirm: null
    };
  },
  methods: {
    confirm() {
      this.$validator.validateAll().then((result) => {
        if (!result) {
          this.$alert.error('Please fill all required fields.');
        }

        AuthController.setPassword({
          password: this.password,
          token: this.token
        });
      });
    }
  }
};
</script>
