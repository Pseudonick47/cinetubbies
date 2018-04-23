export class Movie {
  constructor(data) {
    this.title = '';
    this.genre = '';
    this.director = '';
    this.actors = '';
    this.duration = '';
    this.description = '';
    _.assignWith(this, data);
  }
}
