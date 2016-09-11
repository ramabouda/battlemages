import Vue from 'vue'
import ReconnectingWebSocket from 'reconnecting-websocket'
import {MultiplexedWebsocket, MultiplexedConsumer} from 'battlemages/core/consumer'

import {Authentication} from 'battlemages/core/auth'
import template from './template.jade'


const auth = new Authentication()
if (!auth.isAuthenticated()) {
  window.location = './login'
}

const connectedUsers = {}

const ws = new WebSocket('ws://127.0.0.1:8000/ws/')

// Move this to a root file
const demultiplexer = new MultiplexedWebsocket(ws)

const presenceConsumer = new MultiplexedConsumer('presence')

presenceConsumer.connect = function () {
  this.send({'toto': 'tata'})
}

presenceConsumer.receive = function (message) {
  Object.keys(message).forEach(k => Vue.set(connectedUsers, k, message[k]))
}

demultiplexer.addConsumer(presenceConsumer)

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
