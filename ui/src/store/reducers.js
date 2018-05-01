import { combineReducers } from 'redux'
import {routerReducer} from 'react-router-redux'
import {
  CREATE_USER,
  USER_LOGIN,
  GET_SNACKS,
  SEND_VOTE,
  SEND_SNACK
} from './actions'


function vote(state = {inprocess: false, error: null, remaining: null}, action) {
  switch (action.type) {
    case SEND_VOTE:
      if (action.status === 'success') {
        return {
          ...state,
          inprocess: false,
          error: null,
          remaining: action.data.remaining_votes
        }
      } else if (action.status === 'inprocess') {
        return {
          ...state,
          inprocess: true
        }
      } else if (action.status === 'error') {
        return {
          ...state,
          inprocess: false,
          error: action.error
        }
      } else if (action.status === "clearError") {
        return {
          ...state,
          error: null
        }
      }
      break
    default:
      return state
  }
}


function user(state = {
    login: {
      inprocess: false,
      error: null,
      token: null
    },
    createUser: {
      inprocess: false,
      error: null
    }
  },
  action) {
  switch (action.type) {
    case USER_LOGIN:
      if (action.status === 'inprocess'){
        return {
          ...state,
          login: {
            ...state.login,
            inprocess: true,
          }
        }
      } else if (action.status === 'success') {
        return {
          ...state,
          login: {
            inprocess: false,
            token: action.data,
            error: null
          }
        }
      } else if (action.status === 'error') {
        return {
          ...state,
          login: {
            ...state.login,
            inprocess: false,
            error: action.error
          }
        }
      } else if (action.status === 'clearError') {
        return {
          ...state,
          login: {
            ...state.login,
            error: null
          }
        }
      }
      break
    case CREATE_USER:
      if (action.status === 'inprocess'){
        return {
          ...state,
          createUser: {
            inprocess: true,
            error: null
          },
        }
      } else if (action.status === 'success') {
        return {
          ...state,
          createUser: {
            inprocess: false,
            error: null
          }
        }
      } else if (action.status === 'error') {
        return {
          ...state,
          createUser: {
            inprocess: false,
            error: action.error
          }
        }
      } else if (action.status === 'clearError') {
        return {
          ...state,
          createUser: {
            ...state.createUser,
            error: null
          }
        }
      }
      break
      default:
        return state
  }
}


function snacks(state = {
    inprocess: false,
    error: null,
    items: {
      suggestedCurrent: [],
      suggestedExpired: [],
      permanent: []
    },
    post: {
      inprocess: false,
      error: null
    }
  },
  action) {
  switch (action.type) {
    case GET_SNACKS:
      if (action.status === 'inprocess') {
        return {
          ...state,
          inprocess: true
        }
      } else if (action.status === 'success') {
        return {
          ...state,
          inprocess: false,
          items: action.data,
          error: null
        }
      } else if (action.status === 'error') {
        return {
          ...state,
          inprocess: false,
          error: action.error
        }
      } else if (action.status === 'clearError') {
        return {
          ...state,
          error: null
        }
      }
      break
    case SEND_SNACK:
    if (action.status === 'inprocess') {
      return {
        ...state,
        post: {
          ...state.post,
          inprocess: true,
        }
      }
    } else if (action.status === 'success') {
      return {
        ...state,
        post: {
          ...state.post,
          inprocess: false,
        }
      }
    } else if (action.status === 'error') {
      return {
        ...state,
        post: {
          ...state.post,
          inprocess: false,
          error: action.error,
        }
      }
    } else if (action.status === 'clearError') {
      return {
        ...state,
        post: {
          ...state.post,
          error: null
        }
      }
    }
    break
    default:
      return state
  }
}

export default combineReducers({
  vote,
  user,
  snacks,
  router: routerReducer
})
