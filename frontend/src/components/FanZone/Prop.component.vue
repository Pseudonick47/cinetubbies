<template>
  <v-card
    class="prop grow"
  >
    <div
      class="pb-3"
      style="background-color: black"
    >
      <v-card-media
        src="https://dhs1n389ze6jv.cloudfront.net/img/product-thumb/1518384418b7e5afe78228c751029fa6e1b9063b87.png"
        height="400px"
        contain
        style="-webkit-mask-image:-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,1)), to(rgba(0,0,0,0.2)));"
      />
      <v-container
        class="used-prop-card-body"
        fill-height
        fluid
        pb-0
      >
        <v-layout row>
          <v-flex>
            <v-chip
              v-if="showNew"
              label
              small
              color="yellow darken-11"
              style="transform: scale(0.7);"
            >
              New
            </v-chip>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex
            style="display: flex;"
            pb-3
          >
            <v-card-title
              primary-title
              style="display: flex; align-items: flex-end"
            >
              <div>
                <div class="headline">
                  {{ prop.title }}
                </div>
                <span class="grey--text">{{ prop.category.name }}</span>
              </div>
            </v-card-title>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </v-card>
</template>
<script>
var moment = require('moment');

export default {
  name: 'Prop',
  props: {
    prop: {
      type: Object,
      required: true
    }
  },
  computed: {
    showNew() {
      return moment().diff(moment(this.prop.postDate), 'days') < 7;
    }
  }
};
</script>
<style>

.prop {
  /* padding: 2px 0px; */
  padding-bottom: 2px;
  background: linear-gradient(90deg, rgba(218, 165, 32, 0.2), rgba(230, 175, 37, 0.8), rgba(218, 165, 32, 0.2));
  max-width: 300px;
}

.prop:hover {
  box-shadow: 0px 0px 5px rgba(218, 165, 32, 0.63);
  /* background: radial-gradient(circle, black,#040404, #080808); */
}
.grow {
  transition: all .2s ease-in-out;
}

.grow:hover {
  transform: scale(1.05);
}

.used-prop-card-body {
  position: absolute;
  top: 0;
  left: 0;
  flex-direction: column;
  align-items: flex-start !important;
}

</style>
