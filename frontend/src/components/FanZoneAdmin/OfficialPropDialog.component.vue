<template>
  <div>
    <v-dialog
      v-model="show"
      :fullscreen="isSmallScreen"
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
                :src="prop.image.path"
                class="upload-image"
                contain
                height="100%"
                style="min-height: 200px;"
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
                        v-model="prop.title"
                        :error-messages="errors.collect('title')"
                        name="title"
                        label="Title"
                        type="text"
                        required
                      />
                      <v-select
                        v-validate="'required'"
                        :items="categories"
                        v-model="prop.category"
                        :error-messages="errors.collect('category')"
                        name="category"
                        label="Category"
                        item-text="path"
                        item-value="id"
                        autocomplete
                        return-object
                        required
                      />
                      <v-select
                        v-validate="'required'"
                        :items="theaters"
                        v-model="prop.theater"
                        :error-messages="errors.collect('theater')"
                        name="theater"
                        label="Theater/Cinema"
                        item-text="name"
                        item-value="id"
                        autocomplete
                        return-object
                        required
                      />
                      <v-layout
                        row
                        wrap
                        justify-space-between
                      >
                        <v-flex
                          xs12
                          md5
                        >
                          <v-text-field
                            v-validate="'required|decimal:3'"
                            v-model="prop.price"
                            :error-messages="errors.collect('price')"
                            name="price"
                            label="Price"
                            prefix="$"
                            required
                          />
                        </v-flex>
                        <v-flex
                          xs12
                          md5
                        >
                          <v-text-field
                            v-validate="'required|numeric'"
                            v-model="prop.quantity"
                            :error-messages="errors.collect('quantity')"
                            name="quantity"
                            label="Quantity"
                            required
                          />
                        </v-flex>
                      </v-layout>
                      <small>*indicates required field</small>
                      <v-text-field
                        v-model="prop.description"
                        name="description"
                        label="Description"
                        multi-line
                        style="height: 100%"
                        pa-0
                      />
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
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import MediaService from 'Api/media-upload.service';

import PropsController from 'Controllers/props/official-props.controller';
import TheatersController from 'Controllers/theaters.controller';

import { Prop } from 'Models/prop.model';

export default {
  name: 'OfficialPropDialog',
  props: {
    prop: {
      type: Prop,
      required: false,
      default: () => new Prop()
    }
  },
  data() {
    return {
      show: true,
      selectedCategory: null,
      selectedImage: null,
      selectedTheater: null,
      isSmallScreen: false
    };
  },
  computed: {
    ...mapGetters('props/categories', {
      categories: 'leafs'
    }),
    ...mapGetters({
      theaters: 'systemAdmin/data'
    })
  },
  beforeMount() {
    window.addEventListener('resize', this.changeDialogType);
    TheatersController.requestAllTheaters();
  },
  methods: {
    changeDialogType(e) {
      if (window.outerHeight < 960 || window.outerWidth < 960) {
        this.isSmallScreen = true;
      } else {
        this.isSmallScreen = false;
      }
    },
    showFileDialog() {
      document.getElementById('upload-button').click();
    },
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
      if (this.selectedImage) {
        const reader = new FileReader();

        reader.onload = (e) => {
          this.prop.image.path = e.target.result;
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
          return;
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
      fd.append('kind', 'o');
      fd.append('data', this.selectedImage, this.selectedImage.name);
      return MediaService.postImage(fd);
    },
    saveProp(imageId = null) {
      this.prop.categoryId = this.prop.category.id;
      this.prop.theaterId = this.prop.theater.id;

      if (imageId) {
        this.prop.imageId = imageId;
      }

      if (this.prop.id) {
        this.updateProp();
      } else {
        this.createProp();
      }
    },
    createProp() {
      PropsController.createProp(this.prop)
        .then((response) => {
          this.$alert.success('Official prop successfully created.');
          this.$store.commit('props/official/insertProp', response.data);
          this.reset();
        })
        .catch((e) => {
          this.$alert.error('Something went wrong. Please try again!');
        });
    },
    updateProp() {
      PropsController.updateProp(this.prop.id, this.prop)
        .then((response) => {
          this.$alert.success('Official prop successfully created.');
          this.$store.commit('props/official/updateProp', response.data);
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
