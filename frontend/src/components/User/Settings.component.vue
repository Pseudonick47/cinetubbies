<template>
  <v-flex
    xs-12
    sm5
    pa-4
  >
    <h1>User settings</h1>
    <form>
      <v-text-field
        v-model="user.first_name"
        label="First Name"
      />
      <v-text-field
        v-model="user.last_name"
        label="Last Name"
      />
      <v-text-field
        v-validate="'email'"
        :error-messages="errors.collect('email')"
        v-model="user.email"
        data-vv-name="email"
        label="Email"
      />
      <v-text-field
        v-model="user.city"
        label="City"
      />
      <v-text-field
        v-model="user.phone"
        label="Phone"
      />
      <v-text-field
        v-model="user.password"
        label="New Password"
        type="password"
      />
      <v-text-field
        v-model="user.password_confirmation"
        type="password"
        label="Confirm New Password"
      />
      <v-flex
        xs12
        sm6>
        <v-date-picker
          v-model="user.birth_date"
          year-icon="mdi-calendar-blank"
          prev-icon="mdi-skip-previous"
          next-icon="mdi-skip-next"
        />
      </v-flex>
      <v-btn @click="submit">submit</v-btn>
    </form>
  </v-flex>
</template>

<script>
import UsersController from 'Controllers/users.controller';
import { mapGetters } from 'vuex';

var moment = require('moment');

export default {
  name: 'UserSettings',

  data: () => ({
    user: {}
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ])
  },
  mounted() {
    this.user = _.cloneDeep(this.activeUser);
  },
  methods: {
    submit() {
      let data = _.reduce(this.user, (result, value, key) => {
        if (!_.isEmpty(value)) {
          result[key] = value;
        }
        return result;
      }, {});
      if (data.birth_date) {
        data.birth_date = moment(data.birth_date, 'YYYY-MM-DD').format('YYYY-MM-DDThh:mm');
      }
      this.$validator.validateAll().then((result) => {
        if (result) {
          UsersController.updateUserProfile(data, this.activeUser.id).then((response) => {
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
