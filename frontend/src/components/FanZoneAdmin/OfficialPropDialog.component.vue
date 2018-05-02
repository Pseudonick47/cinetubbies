<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="700px"
  >
    <v-card>
      <v-card-title>
        <span class="headline">New Official Prop</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-container
            fluid
            py-0
          >
            <v-layout
              row
              wrap
              justify-space-between
              align-center
            >
              <v-flex
                xs12
                sm6
                md6
              >
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
                  v-model="selectedCategory"
                  :error-messages="errors.collect('category')"
                  name="category"
                  label="Category"
                  item-text="path"
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
              </v-flex>
              <v-flex
                class="col-stretch"
                xs12
                sm5
                md5
              >
                <v-card
                  color="grey darken-1"
                  class="img-container-stretch white--text"
                >
                  <v-container
                    class="fill-parent"
                    pa-0
                  >
                    <v-layout
                      class="fill-parent"
                      align-center
                      justify-center
                    >
                      <input
                        class="img-button"
                        type="file"
                        @change="imageSelected"
                      >
                      <div class="img-background"/>
                    </v-layout>
                  </v-container>
                </v-card>
              </v-flex>
            </v-layout>
            <v-layout
              row
              mt-3
            >
              <v-text-field
                v-model="prop.description"
                name="description"
                label="Description"
                rows="3"
                multi-line
              />
            </v-layout>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-layout
          row
          justify-space-between
          px-3
          pb-2
        >
          <v-flex
            xs3
            md2
          >
            <v-btn
              block
              @click.native="reset"
            >
              Close
            </v-btn>
          </v-flex>
          <v-flex
            xs3
            md2
          >
            <v-btn
              :disabled="errors.any()"
              block
              @click.native="submit"
            >
              Confirm
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapGetters } from 'vuex';

import { OfficialProp } from 'Models/props/official-prop.model';
import PropsController from 'Controllers/props/official-props.controller';
import MediaService from 'Api/media-upload.service';

export default {
  name: 'OfficialPropDialog',
  data() {
    return {
      show: true,
      prop: new OfficialProp(),
      selectedCategory: null,
      selectedImage: null
    };
  },
  computed: {
    ...mapGetters('props/categories', {
      categories: 'leafs'
    }),
    ...mapGetters({
      admin: 'activeUser'
    })
  },
  methods: {
    imageSelected(event) {
      this.selectedImage = event.target.files[0];
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
        if (result) {
          const fd = new FormData();
          fd.append('kind', 'o');
          fd.append('data', this.selectedImage, this.selectedImage.name);
          MediaService.postImage(fd)
            .then((response) => {
              this.prop.category = this.selectedCategory.id;
              this.prop.image_id = response.data.id;
              this.prop.theater = this.admin.theater.id;

              PropsController.postProp(this.prop)
                .then((response) => {
                  this.$alert.success('Official prop successfully created.');
                  this.$emit('reload');
                  this.reset();
                })
                .catch((e) => {
                  this.$alert.error('Something went wrong. Please try again!');
                });
            })
            .catch((e) => {
              this.$alert.error('Something went wrong. Please try again!');
            });
        } else {
          this.$alert.error('Please fill all required fields.');
        }
      });
    }
  }
};
</script>
<style>
.col-stretch {
  align-self: stretch
}
.fill-parent {
  height: 100%;
}
.img-background {
  width: 100%;
  height: 100%;
  background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgZx-AC-NKhDzPPuvOVfVeK6SPd6bRRJP6rFMXWhO_uqYc7gRw");
  background-size: cover;
  background-repeat: no-repeat;
  filter: grayscale(100%);
  opacity: 0.5;
}
.img-container-stretch {
  height: 100% !important
}
.img-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  z-index: 2;
}
</style>
