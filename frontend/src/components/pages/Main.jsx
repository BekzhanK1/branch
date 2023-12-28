import React, { useState } from 'react'
import Sidebar from '../bars/Sidebar'
import { chartData } from '../../data/chartData'
const Main = () => {
  return (
    <div className='flex relative'>
        <Sidebar/>
        <main className=''>
            <Topbar></Topbar>
        </main>
    </div>
  )
}

export default Main