import ImageHelper from '@/helpers/image-helper';
import { DEFAULT_PROP_IMAGE } from 'Constants/images.constants';

export class Prop {
  constructor(data) {
    _.assign(this, data);

    if (this.image) {
      this.image.path = ImageHelper.getAbsolutePath(this.image.path);
    } else {
      this.image = {};
      this.image.path = ImageHelper.getAbsolutePath(DEFAULT_PROP_IMAGE);
    }

    if (this.kind === 'official') {
      this.category = this.category || {};
      this.theater = this.theater || {};
    }
  }

  update(data) {
    _.assign(this, data);
    this.image.path = ImageHelper.getAbsolutePath(this.image.path);
  }

  clone() {
    return _.cloneDeep(this);
  }
};
