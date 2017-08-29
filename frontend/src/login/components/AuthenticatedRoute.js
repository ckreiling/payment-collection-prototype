import React from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'
import {Redirect, Route} from 'react-router-dom'


/**
 * React functional component for rendering a path that requires authentication. If the
 * user is not authenticated, they will be redirected to the '/login' route.
 * @param Component the component to be rendered
 * @param loggedIn boolean described whether or not the user is logged in
 * @param rest the rest of the props to be passed to the component trying to be rendered
 * @constructor
 */
class _AuthenticatedRoute extends React.Component {

  static propTypes = {
    loggedIn: PropTypes.bool.isRequired,
    component: PropTypes.func.isRequired
  }

  render = () => {
    const Component = this.props.component
    return <Route {...this.props} render={props => (
      this.props.loggedIn
        ? (<Component {...props}/>)
        : (
          <Redirect to={{
            pathname: '/login',
            state: {from: props.location}
          }}/>
        )
    )}/>
  }
}

const mapStateToProps = state => {
  const loggedIn = !!state.token
  return {
    loggedIn
  }
}

const AuthenticatedRoute = connect(mapStateToProps)(_AuthenticatedRoute)

export default AuthenticatedRoute
