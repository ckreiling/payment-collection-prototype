import React, {Component} from 'react';
import store from './store'
import logo from './logo.svg';
import './App.css';
import {login, loggedIn} from "./util/Auth"
import {apiClient} from './util/ApiClient'

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {username: '', password: ''};
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    };

    handleInputChange = function (event) {
        const target = event.target;
        const name = target.name;

        this.setState({
            [name]: target.value
        });
    };

    handleSubmit = function (event) {
        login(this.state.username, this.state.password)
    };

    render() {
        let loginPanel = <div></div>
        if (!loggedIn()) {
            loginPanel = (
                <form>
                    <input type="text" name="username" onChange={this.handleInputChange} />
                    <input type="password" name="password" onChange={this.handleInputChange} />
                    <input type="button" value="SUBMIT" onClick={this.handleSubmit}/>
                </form>
            );
        }
        else {
            loginPanel = 'Your auth token: ' + store.getState().token;
        }
        return (
            <div className="App">
                <div className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <h2>Welcome to React</h2>
                </div>
                <p className="App-intro">
                    To get started, try logging in. In development, this will send a request to localhost:8000.
                </p>
                <p className="App-intro">
                    On a successful login, Redux's state-change logging middleware will display the reassignment of the token in the state.
                </p>
                {loginPanel}
            </div>
        );
    }
}

export default App;
