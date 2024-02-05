import React from 'react'
import { Outlet } from 'react-router'
import Head from '../../bars/Head'
const StaffLayout = () => {
  return (
    <div className='bg-[#DDE1E6] h-full flex-1 text-[#21272A] flex'>
        <div className=' h-full p-[24px] box-border flex-1'>
          <Head title='Staff' sections={[{title:'Customers', id:1, path: 'customers'},{title: 'Workers',id:2,path:'workers'},{title:'KPI',id:3,path:'kpi'}]}></Head>
          <Outlet/>
        </div>
    </div>
  )
}

export default StaffLayout