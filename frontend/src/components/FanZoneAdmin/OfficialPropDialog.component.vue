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
                  v-model="selected_category"
                  label="Category"
                  item-text="name"
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
                      <v-btn
                        class="img-button"
                        small
                      >
                        Upload Image
                      </v-btn>
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

import { OfficialProp } from 'Models/prop.model';

export default {
  name: 'OfficialPropDialog',
  data() {
    return {
      show: true,
      prop: new OfficialProp(),
      selected_category: null
    };
  },
  computed: {
    ...mapGetters('props', {
      categories: 'categories/all'
    })
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
