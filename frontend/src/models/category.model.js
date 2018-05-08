export class Category {
  constructor(data) {
    _.assign(this, data);
    this.subcategories = [];
  }

  isRoot() {
    return this.supercategory == null;
  }
};
