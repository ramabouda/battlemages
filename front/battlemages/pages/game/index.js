import Vue from 'vue'
import ReconnectingWebSocket from 'reconnecting-websocket'

import {Authentication} from 'battlemages/core/auth'
import template from './template.jade'


const auth = new Authentication()
if (!auth.isAuthenticated()) {
  window.location = './login'
}

const connectedUsers = {}

const ws = new WebSocket('ws://127.0.0.1:8000/ws/')
ws.onclose = function () {
}

ws.onopen = function () {
  window.ws = ws
  ws.send(JSON.stringify({
    stream: 'presence',
    payload: {
      'toto': 'tata',
    },
  }))
}

ws.onmessage = function (response) {
  const joined = JSON.parse(response.data).payload
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
      ws.close()
      auth.logout()
      window.location = './login'
    },
  },
})
