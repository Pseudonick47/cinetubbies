<template>
  <v-dialog
    v-model="showThis"
    width="800px"
    persistent
    color="secondary"
    lazy
  >
    <v-card>
      <v-card-title>
        {{ dialogTitle }}
        <v-spacer/>
        <v-text-field
          v-model="selectedAuditorium.name"
          label="Auditorium Name"
          single-line
          autofocus
          hide-details
        />
      </v-card-title>
      <v-card-text>
        <layout
          :seats.sync="selectedAuditorium.layout"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn
          color="error darken-1"
          flat
          @click.native="cancel">Cancel</v-btn>
        <v-btn
          color="info darken-1"
          @click.native="submit">
          Submit
          <v-icon class="ml-2">send</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import Layout from 'Components/Auditorium/Layout.component';

export default {
  name: 'AuditoriumDialog',
  components: {
    Layout
  },
  props: {
    show: {
      type: Boolean,
      required: true
    },
    auditorium: {
      type: Object,
      required: false,
      default: () => ({ name: '', layout: [] })
    }
  },
  data: () => ({
    selectedAuditorium: { name: '', layout: [ [ 1, 1, 1 ], [ 0, 1, 1 ], [ 1, 1, 1 ] ] }
  }),
  computed: {
    showThis: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit('update:show', value);
      }
    },
    dialogTitle() {
      return this.auditorium && this.auditorium.id ?
        'Edit Auditorium' :
        'Add Auditorium';
    }
  },
  mounted() {
    this.selectedAuditorium = this.auditorium || this.selectedAuditorium;
  },
  methods: {
    cancel() {
      this.$emit('cancel');
    },
    submit() {
      this.$emit('auditorium-finished', this.selectedAuditorium);
    }
  }
};
</script>
