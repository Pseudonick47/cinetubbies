<template>
  <div>
    <v-container
      grid-list-md
      text-xs-center>
      <div class="layout-container">
        <div
          v-for="i in rowsCount"
          :key="`4${i}`"
          class="layout-row"
        >
          <div
            v-for="j in colsCount"
            :key="`5${i}${j}`"
            :class="[selectedSeats[i-1][j-1] ? 'seat-free' : 'seat-taken']"
            class="layout-seat"
            @click="seatClicked(i-1, j-1)"
          >
            {{ i-1 }}
            {{ j-1 }}
          </div>
        </div>
      </div>
    </v-container>
  </div>
</template>
<script>
export default {
  name: 'Layout',
  props: {
    seats: {
      type: Array,
      default: () => [ [] ]
    }
  },
  computed: {
    selectedSeats: {
      get() {
        return this.seats;
      },
      set(value) {
        this.$emit('update:seats', value);
      }
    },
    rowsCount() {
      return this.selectedSeats.length;
    },
    colsCount() {
      return this.selectedSeats[0].length;
    }
  },
  methods: {
    seatClicked(i, j) {
      this.selectedSeats[i][j] = this.selectedSeats[i][j] === 1 ? 0 : 1;
      this.$forceUpdate();
    }
  }
};
</script>
<style>
.layout-container {
  height: 70vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}
.layout-row {
  display: flex;
  flex-grow: 1;
  justify-content: flex-start;
  align-items: stretch;
  background: grey;
  padding-left: 4px;
  padding-right: 4px;
}
.layout-row:first-child {
  padding-top: 4px;
}
.layout-row:last-child {
  padding-bottom: 4px;
}

.layout-seat {
  flex: 1;
  margin: 4px 4px 4px 4px;
}
.seat-taken {
  background: crimson;
}
.seat-free {
  background: teal;
}
</style>

