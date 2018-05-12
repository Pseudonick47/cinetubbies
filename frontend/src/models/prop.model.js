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
  }

  update(data) {
    _.assign(this, data);
  }
};
