import * as actionType from '../actions/types'

const initialState = {
  token: null,
  isFetching: false
}

export const login = (state = initialState, action) => {
  switch (action.type) {
    case actionType.REQUEST_TOKEN:
      return {
        ...state,
        isFetching: true
      }
    case actionType.RECEIVE_TOKEN:
      return {
        ...state,
        token: action.token,
        isFetching: false,
        dateReceived: Date.now()
      }
    case actionType.RECEIVE_ERROR:
      return {
        ...state,
        error: action.error,
        isFetching: false
      }
    case actionType.DELETE_TOKEN:
      return initialState
    default:
      return state
  }
}

