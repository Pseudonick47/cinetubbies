const state = {
  movieHeaders: [
    { text: 'Title', sortable: false, value: 'title' },
    { text: 'Genre', sortable: false, value: 'genre' },
    { text: 'Director', sortable: false, value: 'director' },
    { text: 'Actors', sortable: false, value: 'actors' },
    { text: 'Duration(min)', sortable: false, value: 'duration' },
    { text: 'Description', sortable: false, value: 'description' }
  ],
  theaterGenres: [ 'comedy', 'farce', 'satirical', 'tragedy', 'historical', 'musical' ],
  cinemaGenres: [ 'action', 'adventure', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'historical', 'horror', 'mystery', 'philosophical', 'political', 'romance', 'saga', 'satire', 'science fiction', 'social', 'thriller', 'western' ]
};

const getters = {
  movieHeaders: (state) => state.movieHeaders,
  theaterGenres: (state) => state.theaterGenres,
  cinemaGenres: (state) => state.cinemaGenres
};

export {
  state,
  getters
};
