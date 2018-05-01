export class Category {
  constructor(data) {
    _.assignWith(this, data);
    this.subcategories = [];
  }

  isRoot() {
    return this.supercategory == null;
  }
};
