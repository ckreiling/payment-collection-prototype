import axios from 'axios'
import {store} from './store'

/**
 * The following are the URL of the website we are aiming for. Since
 * this is only a project for practicing development, we'll do this.
 * All you have to do to change it to make requests to the same domain
 * is set it to "''".
 * @type {string}
 */
export const URL = 'http://localhost:8000/api/'
export const LOGIN = 'auth/'

export const apiClient = function () {
  const token = store.getState().token

  const params = {
    baseURL: URL,
    headers: {'Authorization': 'Token ' + token}
  }
  return axios.create(params)
}
