
export default {
  screen() {
    const size = window.outerHeight > window.outerWidth ? window.outerWidth : window.outerHeight;

    const screen = {
      xsmall: false,
      small: false,
      medium: false,
      large: false,
      xlarge: false
    };

    if (size <= 600) {
      screen.xsmall = true;
    } else if (size > 600 && size <= 960) {
      screen.small = true;
    } else if (size > 960 && size <= 1264) {
      screen.medium = true;
    } else if (size > 1264 && size <= 1904) {
      screen.large = true;
    } else {
      screen.xlarge = true;
    }

    return screen;
  }
}
;