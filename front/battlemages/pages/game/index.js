import Vue from 'vue'
import ReconnectingWebSocket from 'reconnecting-websocket'

import {Authentication} from 'battlemages/core/auth'
import template from './template.jade'


const auth = new Authentication()
if (!auth.isAuthenticated()) {
  window.location = './login'
}


const ws = new ReconnectingWebSocket('ws://127.0.0.1:8000/ws/?token=' + auth.token)

const connectedUsers = {}
ws.onmessage = function (response) {
  const joined = JSON.parse(response.data)
  Object.keys(joined).forEach(k => Vue.set(connectedUsers, k, joined[k]))
}

export const gameVue = new Vue({
  el: '#app',
  template: template(),
  data: {
    connectedUsers: connectedUsers,
  },
  methods: {
    logout: function () {
      auth.logout()
      window.location = './login'
    },
  },
})
