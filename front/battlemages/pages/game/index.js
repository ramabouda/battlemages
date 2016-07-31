import Vue from 'vue'

import {Authentication} from 'battlemages/core/auth'
import template from './template.jade'


const auth = new Authentication()
if (!auth.isAuthenticated()) {
  window.location = './login'
}


export const gameVue = new Vue({
  el: '#app',
  template: template(),
  data: {},
  methods: {
    logout: function () {
      auth.logout()
      window.location = './login'
    },
  },
})
