<template>
  <v-card
    class="used-prop-card grow"
    color="black"
  >
    <div
      class="pb-4"
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
                  Some text
                </div>
                <span class="grey--text">Also some text</span>
              </div>
            </v-card-title>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </v-card>
</template>

<script>
export default {
  name: 'UsedProp',
  // props: {
  //   info: {
  //     type: Object,
  //     required: true
  //   }
  // },
  // computed: {
  //   category() {
  //     return this.$store.getters['props/categories/one'](this.info.category);
  //   }
  // },
  methods: {
    edit() {
      this.$emit('edit');
    },
    remove() {
      this.$emit('remove');
    }
  }
};
</script>
<style>

.used-prop-card:hover {
  box-shadow: 0px 0px 5px goldenrod;
  /* background-color: #151515 !important; */
  background: radial-gradient(circle, black,#040404, #080808);
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
