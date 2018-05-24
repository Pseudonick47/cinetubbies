<template>
  <v-container>
    <form>
      <v-layout
        row
        wrap
        justify-space-between
      >
        <v-flex
          sm5
          fill-height
        >
          <v-layout row>
            <v-avatar
              v-if="user.image"
              :size="150"
              color="grey lighten-4"
            >
              <img :src="user.getImagePath()">
            </v-avatar>
          </v-layout>
          <v-layout
            row
            mt-3
            mb-2
          >
            <span>Profile picture:</span>
          </v-layout>
          <v-divider/>
          <v-layout
            row
            mt-3
          >
            <input
              type="file"
              @change="imageSelected"
            >
          </v-layout>
        </v-flex>
        <v-flex
          xs-12
          sm6
        >
          <h1>User settings</h1>
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
          <v-layout
            row
            justify-end
            mt-3
            style="height: auto"
          >
            <v-btn @click="submit">submit</v-btn>
          </v-layout>

        </v-flex>
      </v-layout>
    </form>
  </v-container>
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
      let data = _.reduce(
        this.user,
        (result, value, key) => {
          if (!_.isEmpty(value)) {
            result[key] = value;
          }
          return result;
        },
        {}
      );
      this.$validator.validateAll().then(result => {
        if (result) {
          if (this.selectedImage === null) {
            UsersController.updateUserProfile(data, this.user.id)
              .then(response => {
                this.$alert.success('Settings successfully saved');
              })
              .catch(() => {
                this.$alert.error('Error while saving settings');
              });
          } else {
            const fd = new FormData();
            fd.append('kind', 'u');
            fd.append('data', this.selectedImage, this.selectedImage.name);
            MediaService.postImage(fd)
              .then(response => {
                data['image_id'] = response.data.id;
                UsersController.updateUserProfile(data, this.user.id).then(
                  response => {
                    this.$alert.success('Settings successfully saved');
                  }
                );
              })
              .catch(() => {
                this.$alert.error('Error while saving settings');
              });
          }
        }
      });
    }
  }
};
</script>
