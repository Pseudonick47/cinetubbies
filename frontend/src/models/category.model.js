export class Category {
  constructor(data) {
    _.assignWith(this, data);
  }

  isRoot() {
    return this.supercategory == null;
  }
};
