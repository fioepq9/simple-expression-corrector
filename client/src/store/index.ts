import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: {
      id: 'null',
      token: 'null'
    }
  },
  mutations: {
    saveUserInfo (state, payload: {id: string, token: string}) {
      state.userInfo.id = payload.id
      state.userInfo.token = payload.token
    }
  },
  actions: {
  },
  modules: {
  },
  getters: {
    token (state): string {
      return state.userInfo.token
    }
  }
})
