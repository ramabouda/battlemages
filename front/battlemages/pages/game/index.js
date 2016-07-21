import {Authentication} from 'battlemages/core/auth'


const auth = new Authentication()
if (!auth.isAuthenticated()) {
  window.location = './login'
}
