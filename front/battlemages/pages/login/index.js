import {api} from 'battlemages/core/api'
import {TokenManager} from 'battlemages/core/auth'


const tokenManager = new TokenManager()

if (tokenManager.detectAuth()) {
  window.location = './game'
}

api.get('auth_token').then(() => {
  debugger
})






import $ from 'jquery'

$('#app').html('<h1>Login</h1>')
