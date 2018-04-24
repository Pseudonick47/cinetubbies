<template>
  <v-card class="theater-card">
    <v-card-media
      src="http://arab-culture.info/wp-content/uploads/2018/02/1-68.jpg"
      height="200px"
    />
    <v-card-title primary-title>
      <div>
        <div class="headline">{{ info.name }}</div>
        <span class="grey--text">{{ info.address }}</span>
      </div>
    </v-card-title>
    <v-card-text>
      I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
    </v-card-text>
    <v-card-actions>
      <v-layout
        row
        justify-space-between
      >
        <v-btn
          flat
          @click="edit"
        >
          Edit
        </v-btn>
        <v-btn
          flat
          color="purple"
          @click="remove"
        >
          Remove
        </v-btn>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'Theater',
  props: {
    info: {
      type: Object,
      required: true
    }
  },
  methods: {
    edit() {
      this.$emit('editTheater', this.info.id);
    },
    remove() {
      this.$emit('removeTheater', this.info.id);
    }
  }
};
</script>

<style>

.theater-card {
  height: 100% !important;
  justify-content: space-between;
  flex-direction: column;
  display: flex;
}

</style>
