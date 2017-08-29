import * as actionType from './types'
import {LOGIN, URL} from '../../ApiClient'


export const requestToken = () => {
  return {
    type: actionType.REQUEST_TOKEN,
  }
}

export const receiveToken = token => {
  return {
    type: actionType.RECEIVE_TOKEN,
    token
  }
}

export const receiveError = error => {
  return {
    type: actionType.RECEIVE_ERROR,
    error
  }
}

export const deleteToken = () => {
  return {
    type: actionType.DELETE_TOKEN
  }
}

export const fetchToken = (username, password) => dispatch => {
  dispatch(requestToken())

  const data = {
    username,
    password
  }

  return axios.post(URL + LOGIN, data)
    .then(function (response) {
      const token = response.data.token
      dispatch(receiveToken(token))
    })
    .catch(function (error) {
      dispatch(receiveError(error))
    })
}