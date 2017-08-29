import React from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'

import {deleteToken} from "../actions/index"
import Login from "./Login"

class _LoginStatus extends React.Component {

  static propTypes = {
    loggedIn: PropTypes.bool.isRequired,
    logout: PropTypes.func.isRequired
  }

  render = () => (
    this.props.loggedIn
      ? <button value="SIGN OUT" onClick={this.props.logout}/>
      : <div>Please login.</div>
  )
}

const mapStateToProps = state => {
  const loggedIn = !!state.token
  return {
    loggedIn
  }
}

const mapDispatchToProps = dispatch => ({logout: () => dispatch(deleteToken())})

const LoginStatus = connect(mapStateToProps, mapDispatchToProps)(_LoginStatus)

export default LoginStatus