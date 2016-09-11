import 'whatwg-fetch' // polyfill for the fetch api if needed
import restful, { fetchBackend } from 'restful.js'

export const api = restful(window.__SETTINGS__.app.api_url, fetchBackend(window.fetch))
