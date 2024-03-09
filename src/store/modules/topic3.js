const state = {
    dataset: ""
  }
  
  const mutations = {
    SET_DATASET: (state, dataset) => {
      state.dataset = dataset
    }
  }
  
  const actions = {
    setDataset({ commit }, dataset) {
      commit('SET_DATASET', dataset)
    }
  }
  
  export default {
    namespaced: true,
    state,
    mutations,
    actions
  }
  