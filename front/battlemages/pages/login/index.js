import Vue from 'vue'

import {Authentication} from 'battlemages/core/auth'
import loginTemplate from './template.jade'


const auth = new Authentication()
if (auth.isAuthenticated()) {
  window.location = './game'
}


export const loginVue = new Vue({
  el: '#app',
  template: loginTemplate(),
  data: {
    username: '',
    password: '',
    error: '',
  },
  methods: {
    login: function (event) {
      event.preventDefault()
      auth.authenticate({
        username: this.username,
        password: this.password,
      })
        .then(() => (window.location = './game'))
        .catch(error => (this.error = error.message))
    },
  },
})

