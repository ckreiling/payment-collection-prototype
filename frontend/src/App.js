import React, {Component} from 'react'
import {BrowserRouter, Redirect, Route} from 'react-router-dom'
import './App.css'
import Login from "./login/components/Login"
import AuthenticatedRoute from "./login/components/AuthenticatedRoute"
import LoginStatus from './login/components/LoginStatus'
import {Dashboard} from "./dashboard/components"

class App extends Component {
  render = () => (
    <BrowserRouter>
      <div>
        <LoginStatus/>
        <Route path="/" render={() => <Redirect to="/dashboard"/>}/>
        <Route path="/login" component={Login}/>
        <AuthenticatedRoute path="/dashboard" component={Dashboard}/>
      </div>
    </BrowserRouter>
  )
}

export default App
