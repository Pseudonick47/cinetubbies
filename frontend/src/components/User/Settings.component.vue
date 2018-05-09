<template>
  <v-flex
    xs-12
    sm5
    pa-4
  >
    <v-card>
      <v-card-media
        v-if="user.image"
        :src="user.getImagePath()"
        height="200px"
      />
    </v-card>
    <h1>User settings</h1>
    <form>
      <v-layout row>
        <span>Profile picture:</span>
        <v-divider/>
        <input
          type="file"
          @change="imageSelected"
      ></v-layout>
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
import MediaService from 'Api/media-upload.service';

var moment = require('moment');

export default {
  name: 'UserSettings',

  data: () => ({
    selectedImage: null
  }),
  computed: {
    ...mapGetters({
      user: 'activeUser'
    })
  },
  methods: {
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
    },
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
          if (this.selectedImage === null) {
            UsersController.updateUserProfile(data, this.user.id).then((response) => {
              this.$alert.success('Settings successfully saved');
            }).catch(() => {
              this.$alert.error('Error while saving settings');
            });
          } else {
            const fd = new FormData();
            fd.append('kind', 'u');
            fd.append('data', this.selectedImage, this.selectedImage.name);
            MediaService.postImage(fd)
              .then((response) => {
                data['image_id'] = response.data.id;
                UsersController.updateUserProfile(data, this.user.id)
                  .then((response) => {
                    this.$alert.success('Settings successfully saved');
                  });
              }).catch(() => {
                this.$alert.error('Error while saving settings');
              });
          }
        }
      });
    }
  }
};
</script>
