import cookies from 'js-cookie'

import {api as battlemagesApi} from 'battlemages/core/api'


export class Authentication {
  constructor ({
    cookieName = 'sessionid',
    api = battlemagesApi,
  } = {}) {
    this.api = api
    this.cookieName = cookieName
  }

  get sessionId () {
    return cookies.get(this.cookieName)
  }

  set sessionId (sessionId) {
    cookies.set(this.cookieName, sessionId)
    // this.api.header('X-CSRFToken', 'Bearer ' + this.token)
  }

  isAuthenticated () {
    return !!this.sessionId
  }

  authenticate (credentials) {
    this.api.header('Authorization', 'Basic ' + btoa(credentials.username + ':' + credentials.password))
    return this.api.custom('authentication/').post().then(response => {
      const data = response.body().data()
      this.sessionId = data.sessionid
    })
  }

  logout () {
    cookies.remove(this.cookieName)
    // TODO(raph): also remove the session from the server
  }

  // TODO(raph): refresh auth once in a while, to avoid being disconnected while in a game
}
