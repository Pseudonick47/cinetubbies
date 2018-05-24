<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="800px"
  >
    <v-card color="black">
      <v-container pa-0>
        <v-layout
          row
          wrap
        >
          <v-flex
            class="upload-container"
            xs12
            sm12
            md4
            px-4
          >
            <v-card-media
              :src="showImage"
              class="upload-image"
              contain
              height="100%"
            />
            <div class="upload-button-container">
              <v-btn
                @click="showFileDialog"
              >
                Open Image
              </v-btn>
              <input
                id="upload-button"
                type="file"
                style="display: none"
                @change="imageSelected"
              >
            </div>
          </v-flex>
          <v-flex
            xs12
            sm12
            md8
          >
            <v-container class="prop-info-body">
              <v-layout
                row
                wrap
              >
                <v-card-title>
                  <span class="headline prop-info-highlight">Used Prop</span>
                </v-card-title>
              </v-layout>
              <v-divider class="prop-info-divider mt-1 mb-3"/>
              <v-layout
                row
                wrap
                px-4
              >
                <v-flex>
                  <v-form ref="form">
                    <v-text-field
                      v-validate="'required'"
                      v-model="data.title"
                      :error-messages="errors.collect('title')"
                      name="title"
                      label="Title"
                      type="text"
                      required
                    />
                    <v-select
                      v-validate="'required'"
                      :items="categories"
                      v-model="data.category"
                      :error-messages="errors.collect('category')"
                      name="category"
                      label="Category"
                      item-text="path"
                      autocomplete
                      return-object
                      required
                    />
                    <v-menu
                      ref="menu"
                      :close-on-content-click="false"
                      v-model="menu"
                      :nudge-right="40"
                      lazy
                      transition="scale-transition"
                      offset-y
                      full-width
                      min-width="290px"
                    >
                      <v-text-field
                        slot="activator"
                        v-model="data.expirationDate"
                        label="Expiration date"
                        prepend-icon="event"
                        readonly
                      />
                      <v-date-picker
                        v-model="data.expirationDate"
                        color="teal"
                        no-title
                        scrollable
                      />
                    </v-menu>
                    <v-text-field
                      v-model="data.description"
                      name="description"
                      label="Description"
                      rows="3"
                      multi-line
                    />
                    <small>*indicates required field</small>
                  </v-form>
                </v-flex>
              </v-layout>
              <v-layout
                row
                justify-end
                pb-2
              >
                <v-flex
                  xs4
                  md3
                >
                  <v-btn
                    class="prop-info-highlight"
                    flat
                    @click.native="reset"
                  >
                    Close
                  </v-btn>
                </v-flex>
                <v-flex
                  xs4
                  md3
                >
                  <v-btn
                    :disabled="errors.any()"
                    class="prop-info-highlight"
                    flat
                    @click.native="submit"
                  >
                    Confirm
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapGetters } from 'vuex';

import { Prop } from 'Models/prop.model';
import PropsController from 'Controllers/props/used-props.controller';
import MediaService from 'Api/media-upload.service';

export default {
  name: 'UsedPropDialog',
  props: {
    prop: {
      type: Prop,
      required: false,
      default: () => new Prop({ kind: 'U' })
    }
  },
  data() {
    return {
      show: true,
      data: this.prop.clone(),
      selectedCategory: null,
      selectedImage: null,
      menu: null,
      showImage: this.prop.image.path
    };
  },
  computed: {
    ...mapGetters('props/categories', {
      categories: 'leafs'
    }),
    ...mapGetters({
      user: 'activeUser'
    })
  },
  methods: {
    showFileDialog() {
      document.getElementById('upload-button').click();
    },
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
      if (this.selectedImage) {
        const reader = new FileReader();

        reader.onload = (e) => {
          this.showImage = e.target.result;
        };

        reader.readAsDataURL(this.selectedImage);
      }
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
        if (!result) {
          this.$alert.error('Please fill all required fields.');
        }

        if (this.selectedImage) {
          this.postImage()
            .then((response) => {
              this.saveProp(response.data.id);
            })
            .catch(() => {
              this.$alert.error('Image upload failed. Please check your internet connection and try again!');
            });
        } else {
          this.saveProp();
        }
      });
    },
    postImage() {
      const fd = new FormData();
      fd.append('kind', 'z');
      fd.append('data', this.selectedImage, this.selectedImage.name);
      return MediaService.postImage(fd);
    },
    saveProp(imageId = null) {
      this.data.categoryId = this.data.category.id;
      this.data.ownerId = this.user.id;

      if (imageId) {
        this.data.imageId = imageId;
      }

      if (this.data.id) {
        this.updateProp();
      } else {
        this.createProp();
      }
    },
    createProp() {
      PropsController.postProp(this.data)
        .then((response) => {
          this.$alert.success('Used prop successfully created.');
          this.$store.commit('props/insertProp', response.data);
          this.reset();
        })
        .catch((e) => {
          this.$alert.error('Something went wrong. Please try again!');
        });
    },
    updateProp() {
      PropsController.updateProp(this.data.id, this.data)
        .then((response) => {
          this.$alert.success('Used prop successfully created.');
          this.prop.update(response.data);
          this.reset();
        })
        .catch((e) => {
          this.$alert.error('Something went wrong. Please try again!');
        });
    }
  }
};
</script>
<style>
.prop-info-body {
  height: 100% !important;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-content: space-between;
}

.prop-info-highlight {
  color: #daa520 !important;
}

.prop-info-divider {
  background: linear-gradient(90deg, black, #424242, #c5951b, #424242, black);
}

.upload-button-container {
  width: 100%;
  height: 100%;
  transform: translate(0, -100%);
  -ms-transform: translate(0, -100%);
  z-index: 2;
  opacity: 0;
  transition: .5s ease;

  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  z-index: 2;
}

.upload-image {
  transition: .5s ease;
}

.upload-container:hover .upload-button-container {
  opacity: 1;
}

.upload-container:hover .upload-image {
  opacity: 0.3;
}
</style>
