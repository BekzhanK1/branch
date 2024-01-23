import React from 'react'
import Head from '../Storage/Head'
import Analytics from './Analytics'
import Sidebar from '../../bars/Sidebar'
import { useState } from 'react'
const Main = () => {
  const [currentState, setCurrentState] = useState('Analytics')
  return (
    <div className='bg-[#DDE1E6] h-full w-full text-[#21272A] flex'>
        <Sidebar></Sidebar>
        <div className='w-full h-full p-[24px]'>
          <Head title='Main Page' sections={['Cell','Cell','Analytics','Cell']}></Head>
          <div className='w-fit h-fit'>
              {currentState==='Analytics' && <Analytics/>}
          </div>
        </div>
    </div>
  )
}

export default Main