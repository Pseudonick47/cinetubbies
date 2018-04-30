<template>
  <div>
    <v-dialog
      v-model="editDialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title>
          Change information
        </v-card-title>
        <v-card-text>
          <v-form
            v-model="valid"
          >
            <v-text-field
              v-validate="'required'"
              v-model="movie.title"
              :error-messages="errors.collect('title')"
              :counter="255"
              label="Title"
              data-vv-name="title"
              required
            />
            <v-text-field
              :counter="255"
              v-model="movie.genre"
              :error-messages="errors.collect('genre')"
              label="Genre"
              data-vv-name="genre"
              required
            />
            <v-text-field
              :counter="255"
              v-model="movie.director"
              label="Director"
            />
            <v-text-field
              :counter="255"
              v-model="movie.actors"
              label="Actors"
            />
            <v-text-field
              :counter="255"
              v-model="movie.duration"
              label="Duration"
            />
            <v-text-field
              :counter="255"
              v-model="movie.description"
              label="Description"
            />
            <!--<v-btn
              :disabled="!valid"
              @click="edit(movie.title, movie.genre, movie.director, movie.actors, movie.duration, movie.description)"
            >
              save
            </v-btn>-->
            <v-btn @click="editdialog=false">close</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: {
    'valid': {
      type: Boolean,
      required: true
    },
    'movie': {
      type: String,
      required: true
    },
    'editDialog': {
      type: String,
      required: true
    }
  }
};
</script>

