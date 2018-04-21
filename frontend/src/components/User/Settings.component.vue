<template>
  <v-flex
    xs-12
    sm5
  >
    <h1>User settings</h1>
    <form>
      <v-text-field
        v-model="first_name"
        label="First Name"
      />
      <v-text-field
        v-model="last_name"
        label="Last Name"
      />
      <v-flex
        xs12
        sm6>
        <v-date-picker
          v-model="birth_date"
          year-icon="mdi-calendar-blank"
          prev-icon="mdi-skip-previous"
          next-icon="mdi-skip-next"
        />
      </v-flex>
      <!-- password = models.CharField(max_length=255) -->
      <v-btn @click="submit">submit</v-btn>
    </form>
  </v-flex>
</template>

<script>
import UsersController from 'Controllers/users.controller';
import { mapGetters } from 'vuex';

export default {
  name: 'UserSettings',

  data: () => ({
    birth_date: null,
    first_name: '',
    last_name: ''
  }),
  computed: {
    ...mapGetters([
      'activeUser'
    ])
  },
  mounted() {
    this.birth_date = this.activeUser.birth_date;
    this.first_name = this.activeUser.first_name;
    this.last_name = this.activeUser.last_name;
  },
  methods: {
    submit() {
      let data = { first_name: this.first_name, last_name: this.last_name, birth_date: this.birth_date };
      UsersController.updateUserProfile(data, this.activeUser.id).then((response) => {
        this.$alert.success('Settings successfully saved');
      }).catch(() => {
        this.$alert.error('Error while saving settings');
      });
    }
  }
};
</script>
