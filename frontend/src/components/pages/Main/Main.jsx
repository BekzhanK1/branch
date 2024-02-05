import React from 'react'
import Head from '../../bars/Head'
import Analytics from './Analytics'
import Sidebar from '../../bars/Sidebar'
import { useState } from 'react'
import { Outlet } from 'react-router'
const Main = () => {
  const [currentState, setCurrentState] = useState('Analytics')
  return (
    <div className='bg-[#DDE1E6] h-full flex-1 text-[#21272A] flex'>
        <div className=' h-full p-[24px] box-border flex-1'>
          <Head title='Main Page' sections={[{title:'Cell', id:1, path: 'cell1'},{title: 'Cell',id:2,path:'cell2'},{title:'Analytics',id:3,path:'analytics'},{title:'Cell',id:4,path:'cell4'}]}></Head>
          <Outlet/>
        </div>
    </div>
  )
}

export default Main