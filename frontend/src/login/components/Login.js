import React from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'
import {Redirect, Route} from 'react-router-dom'
import {fetchToken} from "../actions/index"

// Call this as a function in usage - React will render it about 50% faster.
const LoginErrorBox = (errorText) => (
  errorText
    ? null
    : <div>{errorText}</div>
)

class _Login extends React.Component {

  static propTypes = {
    // The user's login token stored in the state.
    token: PropTypes.string.isRequired,
    // Is the state fetching the token (logging the user in)?
    isFetching: PropTypes.bool.isRequired,
    // login function callback takes username and password
    login: PropTypes.func.isRequired,
    // The error message
    error: PropTypes.string,
  }

  constructor(props) {
    super(props)
    this.username = ''
    this.password = ''
  }

  render = () => (
    this.props.token
      ? <Redirect to="/dashboard"/>
      :
      <form>
        {LoginErrorBox(this.props.error)}
        <input type="text" value={this.username}/>
        <input type="password" value={this.password}/>
        <input type="button" value="SUBMIT" onClick={this.props.login(this.username, this.password)}/>
      </form>
  )
}

const mapStateToProps = state => {
  const {token, isFetching, error} = state
  return {
    token, isFetching, error
  }
}

const mapDispatchToProps = dispatch => {
  return {
    login: (username, password) => {
      dispatch(fetchToken(username, password))
    }
  }
}

const Login = connect(mapStateToProps, mapDispatchToProps)(_Login)

export default Login
