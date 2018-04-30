import Axios from 'axios';

const PREFIX = 'fan-zone/';
const OFFICIAL_PROPS = 'official-props/';

export default {
  fetchOfficialProps(num, page) {
    return Axios.get(`${PREFIX}${OFFICIAL_PROPS}?num=${num}&page=${page}`);
  },

  fetchOfficialPropsCount() {
    return Axios.get(`${PREFIX}${OFFICIAL_PROPS}count`);
  }
};
