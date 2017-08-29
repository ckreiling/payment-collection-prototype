import axios from 'axios'
import _ from 'lodash'
import {store} from '../../store'
import {deleteToken, setToken} from '../actions'
import {LOGIN, URL} from '../../ApiClient'

export function InvalidCredentialsException(message) {
  this.message = message
  this.name = 'InvalidCredentialsException'
}

export function logout() {
  store.dispatch(deleteToken())
}

export function login(username, password) {
  const data = {
    username,
    password
  }
  return axios
  .post(URL + LOGIN, data)
  .then(function (response) {
    store.dispatch(setToken(response.data.token))
  })
  .catch(function (error) {
    // raise different exception if due to invalid credentials
    if (_.get(error, 'response.status') === 400) {
      throw new InvalidCredentialsException(error)
    }
    console.log('Unsuccessful login')
    throw error
  })
}

export const loggedIn = () => store.getState().token