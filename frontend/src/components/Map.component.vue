<template>
  <GmapMap
    :zoom="zoom"
    :center="center"
    :options="options"
    style="width: 100%; height: 500px;"
    @center_changed="updateCenter"
    @idle="sync">
    <GmapMarker
      v-if="marker"
      :position="marker"
      label="★"
    />
  </GmapMap>
</template>
<script>
export default {
  name: 'GMap',
  props: {
    cinema: {
      type: Object,
      required: false,
      default: () => ({ lat: 45.259452791770826, lng: 19.82699662833079 })
    },
    readOnly: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    center: { lat: 45.259452791770826, lng: 19.82699662833079 },
    reportedMapCenter: { lat: 45.259452791770826, lng: 19.82699662833079 },
    zoom: 15,
    options: {
      componentRestrictions: { country: 'rs' }
    }
  }),
  computed: {
    marker() {
      if (this.readOnly) {
        return this.cinema;
      }
      return this.reportedMapCenter;
    }
  },
  created() {
    setTimeout(() => {
      this.reportedMapCenter = this.cinema;
      this.sync();
    }, 100);
  },
  methods: {
    updateCenter(latLng) {
      this.reportedMapCenter = {
        lat: latLng.lat(),
        lng: latLng.lng()
      };
    },
    sync() {
      this.center = this.reportedMapCenter;
    }
  }
};
</script>
