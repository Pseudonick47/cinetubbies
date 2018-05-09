const state = {
  movieHeaders: [
    { text: 'Title', sortable: false, value: 'title' },
    { text: 'Genre', sortable: false, value: 'genre' },
    { text: 'Director', sortable: false, value: 'director' },
    { text: 'Actors', sortable: false, value: 'actors' },
    { text: 'Duration(min)', sortable: false, value: 'duration' },
    { text: 'Description', sortable: false, value: 'description' }
  ]
};

const getters = {
  movieHeaders: (state) => state.movieHeaders
};

export {
  state,
  getters
};
