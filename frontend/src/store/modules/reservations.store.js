import * as _ from 'lodash';
import { Reward } from 'Models/reward.model';

const namespaced = true;

const state = {
  basic: new Reward({ status: 'basic', min: 0, max: 24 }),
  bronze: new Reward({ status: 'bronze', min: 25, max: 49 }),
  silver: new Reward({ status: 'silver', min: 50, max: 74 }),
  gold: new Reward({ status: 'gold', min: 75, max: 100 })
};

const getters = {
  basic: (state) => state.basic,
  bronze: (state) => state.bronze,
  silver: (state) => state.silver,
  gold: (state) => state.gold,
  all: (state) => [ state.basic, state.bronze, state.silver, state.gold ]
};

const mutations = {
  setRewards(state, data) {
    _.each(data, (reward) => {
      state[reward.status] = new Reward(reward);
    });
  }
};

export {
  namespaced,
  state,
  getters,
  mutations
};
