import {API_URL} from '../settings'
import {push} from 'react-router-redux'



export const CREATE_USER = 'CREATE_USER'

export function createUser(detail) {
  return {
    type: CREATE_USER,
    ...detail
  }
}

export const USER_LOGIN = 'USER_LOGIN'

export function userLogin(detail) {
  return {
    type: USER_LOGIN,
    ...detail
  }
}

export const GET_SNACKS = 'GET_SNACKS'

export function getSnacks(detail) {
  return {
    type: GET_SNACKS,
    ...detail
  }
}

export const SEND_SNACK = 'SEND_SNACK'

export function sendSnack(detail) {
  return {
    type: SEND_SNACK,
    ...detail
  }
}

export const SEND_VOTE = 'SEND_VOTE'

export function sendVote(detail) {
  return {
    type: SEND_VOTE,
    ...detail
  }
}


export function doCreateUser(user) {
  return function(dispatch) {
    // let state know we have started creating a user
    dispatch(createUser({status: 'inprocess'}))
    return fetch(API_URL + 'users', {
      method: 'POST',
      body: JSON.stringify(user),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    }).then(
      res => res.json()
      .then(function(json) {
        if (!res.ok) {
          dispatch(createUser({status: 'error', error: json.error}))
        } else {
          dispatch(createUser({status: 'success'}))
          dispatch(push('/login'))
        }
      }
    ))
  }
}

export function doLoginUser(user) {
  return function(dispatch) {
    // let state know we have started creating a user
    dispatch(userLogin({status: 'inprocess'}))
    return fetch(API_URL + 'login', {
      method: 'POST',
      body: JSON.stringify(user),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    }).then(
      res => res.json()
      .then(function(json) {
        if (!res.ok) {
          dispatch(userLogin({status: 'error', error: json.error}))
        } else {
          // store token in session storage
          sessionStorage.setItem('token', json.data.token)
          dispatch(userLogin({status: 'success'}))
          dispatch(push('/vote'))
        }
      }
    ))
  }
}

export function doGetSnacks() {
  return function(dispatch) {
    // check if token is in session storage, or redirect to login
    var token = sessionStorage.getItem('token')
    if (!token) {
      dispatch(push('/login'))
    }
    // start getSnacks
    dispatch(getSnacks({status: 'inprocess'}))
    return fetch(API_URL + 'snacks', {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    }).then(res => res.json()
    .then(function(json) {
      if (!res.ok) {
        dispatch(getSnacks({status: 'error', error: json.error}))
      } else {
        dispatch(getSnacks({status: 'success', data: json.data}))
      }
    }))
  }
}

export function doSendVote(snack) {
  return function(dispatch) {
    // check if token is in session storage, or redirect to login
    var token = sessionStorage.getItem('token')
    if (!token) {
      dispatch(push('/login'))
    }
    //start sendVote
    dispatch(sendVote({status: 'inprocess'}))
    return fetch(API_URL + 'vote',{
        method: 'POST',
        headers: new Headers({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }),
        body: JSON.stringify(snack)
    }).then(res => res.json()
    .then(function (json) {
      if (!res.ok) {
        dispatch(sendVote({status: 'error', error: json.error}))
      } else {
        dispatch(sendVote({status: 'success', data: json.data}))
        // refresh votes
        dispatch(doGetSnacks())
      }
    }))
  }
}

export function doSendSnack(snack) {
  return function(dispatch) {
    // check if token is in session storage, or redirect to login
    var token = sessionStorage.getItem('token')
    if (!token) {
      dispatch(push('/login'))
    }
    dispatch(sendSnack({status: 'inprocess'}))
    return fetch(API_URL + 'snacks',{
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }),
      body: JSON.stringify(snack)
    }).then(res => res.json()
    .then(function(json) {
      if (!res.ok) {
        dispatch(sendSnack({status: 'error', error: json.error}))
      } else {
        dispatch(sendSnack({status: 'success'}))
        // send you to vote page after suggestion
        dispatch(push("/vote"))
      }
    }))
  }
}
