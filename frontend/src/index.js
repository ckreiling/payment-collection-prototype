import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import AppProvider, {store} from './store'
import {Provider} from 'react-redux'
import registerServiceWorker from './registerServiceWorker'

const AppReduxProvider = () => <Provider store={store}><AppProvider/></Provider>

ReactDOM.render(<AppReduxProvider/>, document.getElementById('root'))
registerServiceWorker()
