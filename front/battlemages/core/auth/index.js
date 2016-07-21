import jwtDecode from 'jwt-decode'
import cookies from 'js-cookie'

import {api as battlemagesApi} from 'battlemages/core/api'


export class Authentication {
  constructor ({
    tokenName = 'auth_token',
    api = battlemagesApi,
  } = {}) {
    this.api = api
    this.token = null
    this.tokenName = tokenName
    this.tokenData = {}
    this.tokenRefreshTimeoutId = null
    this.detectToken()
  }

  setToken (_token) {
    this.token = _token
    this.tokenData = jwtDecode(_token)
    this.api.header('Authorization', 'Bearer ' + this.token)
    cookies.set(this.tokenName, this.token)
    this.tokenRefreshTimeoutId = setTimeout(this.refresh.bind(this), this.tokenTimeLeft())
  }

  tokenTimeLeft () {
    return this.tokenData.exp * 1000 - Date.now()
  }

  detectToken () {
    const foundToken = cookies.get(this.tokenName)
    if (foundToken) {
      this.setToken(foundToken)
      if (this.tokenTimeLeft() < 0) {
        this.logout()
        return false
      }
      return true
    }
    return false
  }

  isAuthenticated () {
    return !!this.token
  }

  authenticate (credentials) {
    return this.api.custom('auth_token/').post(credentials).then(response => {
      const data = response.body().data()
      this.setToken(data.token)
    })
  }

  logout () {
    cookies.remove(this.tokenName)
    clearTimeout(this.tokenRefreshTimeoutId)
    this.tokenData = {}
    this.token = null
    this.tokenRefreshTimeoutId = null
  }

  // TODO(raphael): Handle the refresh
  refresh () {
    this.api.custom('auth_token_refresh/').post({token: this.token}).then(response => {
      const data = response.body().data()
      this.setToken(data.token)
    })
  }
}
