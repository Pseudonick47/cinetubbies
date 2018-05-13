<template>
  <v-card
    class="prop-info-card grow-card"
    color="black"
  >
    <v-container pa-0>
      <v-layout
        row
        wrap
      >
        <v-flex
          xs12
          sm12
          md4
          pl-4
        >
          <v-card-media
            v-if="info.image"
            :src="info.image.path"
            contain
            height="100%"
            style="-webkit-mask-image:-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,1)), to(rgba(0,0,0,0.5)));"
          />
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
              justify-space-between
              pr-4
              pl-3
              mt-4
              mb-2
            >
              <div class="display-1">{{ info.title }}</div>
              <div v-if="status">
                <v-icon
                  v-if="!info.approved && info.pendingApproval"
                  class="prop-info-highlight"
                >hourglass_empty</v-icon>
                <v-icon
                  v-else-if="!info.approved && !info.pendingApproval"
                  class="prop-info-highlight"
                >report</v-icon>
                <v-icon
                  v-else
                  class="prop-info-highlight"
                >done_all</v-icon>
              </div>
            </v-layout>
            <v-divider class="prop-info-divider mt-1 mb-3"/>
            <v-layout
              class="prop-info-item"
              row
              wrap
              px-4
              py-1
              mb-0
            >
              <div class="subheading">
                <p style="text-align: justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor felis at mollis blandit. Etiam quam dui, pharetra ac ligula ut, varius venenatis metus. Curabitur eget efficitur nisi. Proin commodo efficitur tortor vel vulputate. Nam ipsum dolor, pulvinar at vehicula sit amet, porttitor a nisi. Donec congue tristique justo ac fringilla.</p>
              </div>
              <div
                class="caption grey--text"
                style="width: 100%"
              >
                <p class="text-xs-right">Expiration date: {{ info.expirationDate }}</p>
              </div>
            </v-layout>
            <v-layout
              row
              wrap
            >
              <v-card-actions
                class="prop-info-item"
              >
                <v-layout
                  row
                  wrap
                  justify-end
                >
                  <v-btn
                    v-for="action in actions"
                    :key="action"
                    class="prop-info-highlight"
                    flat
                    @click="clicked(action)"
                  >{{ action }}</v-btn>
                </v-layout>
              </v-card-actions>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>
<script>
import { Prop } from 'Models/prop.model';

export default {
  name: 'UsedProp',
  props: {
    info: {
      type: Prop,
      required: true
    },
    actions: {
      type: Array,
      required: false,
      default: () => []
    },
    status: {
      type: Boolean,
      required: false,
      default: () => false
    }
  },
  methods: {
    clicked(e) {
      this.$emit('clicked', { prop: this.info, action: e });
    }
  }
};
</script>
