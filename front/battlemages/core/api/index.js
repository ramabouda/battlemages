import 'whatwg-fetch' // polyfill for the fetch api
import restful, { fetchBackend } from 'restful.js'

export const api = restful(window.__SETTINGS__.app.api_url, fetchBackend(window.fetch))
