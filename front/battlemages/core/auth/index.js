import jwtDecode from 'jwt-decode'
import cookies from 'js-cookie'

import {api as battlemagesApi} from 'battlemages/core/api'


export class TokenManager {
  constructor ({
    tokenName = 'auth_token',
    api = battlemagesApi,
  } = {}) {
    this.api = api
    this.token = null
    this.tokenName = tokenName
    this.tokenData = {}
  }

  setToken (_token) {
    this.token = _token
    this.tokenData = jwtDecode(_token)
    this.api.header('Authorization', 'JWT ' + this.token)
    cookies.set(this.tokenName, this.token)
  }

  isAuthenticated () {
    return !!cookies.get(this.tokenName)
  }

  detectAuth () {
    if (this.isAuthenticated()) {
      this.setToken(cookies.get(this.tokenName))
      return true
    }
    return false
  }
}
