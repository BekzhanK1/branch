import React from 'react'
import Sidebar from './components/bars/Sidebar'
import { Outlet } from 'react-router'
import classes from './RootLayout.module.css'
import store from './components/store/store'
import { Provider } from 'react-redux'
const RootLayout = () => {
  return (
    <Provider store={store}>
      <div className={classes.content}>
          <Sidebar/>
          <Outlet/>
      </div>
    </Provider>
  )
}

export default RootLayout