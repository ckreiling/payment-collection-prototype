import React from 'react'
import {store} from '../../store'

export const Dashboard = () => <div>You've reached the dashboard! Your auth token is {store.getState().token}</div>