import React, { useEffect, useState } from 'react'
import './Storage.css'
import Head from './Head'
import InfoBar from './InfoBar'
import Sidebar from '../../bars/Sidebar'
const Storage = () => {

  const [showProductPages,setShowProductPages] = useState([1,2,3,4,5])
  const [currentPage, setCurrentPage] = useState(1)
  const [pagesLength, setPagesLength] = useState(11)
  console.log(showProductPages)
  console.log(currentPage)
  useEffect(()=>{
    if (currentPage<pagesLength-1){
      if (currentPage==1 || currentPage==2){
        setShowProductPages([1,2,3,4,5])
      }else{
        setShowProductPages([currentPage-2,currentPage-1,currentPage,currentPage+1,currentPage+2])
      }
    }
  },[currentPage])

  const handleNextPage = () => {
    if (currentPage<11){
      setCurrentPage(prev=>prev+1)
    }
  }

  const handlePreviousPage = () => {
    if (currentPage>1){
      setCurrentPage(prev=>prev-1)
    }
  }
  return (
    <div className='bg-[#DDE1E6] h-full w-full text-[#21272A] flex relative'>
      <Sidebar/>
      <div className='w-full h-full p-[24px]'>
        <Head title='Storage' sections={['Cell','Cell','Cell','Cell']}></Head>
        <section className='w-full flex gap-[20px]'>
          <InfoBar textType='Number of duties' info='117 out of 180' style='flex-1'/>
          <InfoBar textType='Current price' info='4 145 147 tenge' style='flex-1'/>
          <InfoBar textType='Total price' info='31 145 000 tenge' style='flex-1'/>
        </section>
        <div className='m-[20px] h-[60vh]'>
          <table className='w-full text-left text-[14px]'>
            <thead>
              <tr>
                <th className='w-[32%]'>Name</th>
                <th>Date</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total Price</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className='w-[32%]'>Ароматизаторы для табака</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Badge</td>
              </tr>
              <tr>
                <td className='w-[32%]'>Ароматизаторы для табака</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Badge</td>
              </tr>
              <tr>
                <td className='w-[32%]'>Ароматизаторы для табака</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Cell Text</td>
                <td>Badge</td>
              </tr>
            </tbody>
          </table>
          <section className='m-auto max-w-[50%] flex justify-center mt-4'>
            <button className='bg-inherit border-0' onClick={handlePreviousPage}>Previous</button>
            <ul className='flex justify-center align-middle w-[45%]'>
              {showProductPages.map(page=>{
                let cssClasses = 'flex-1 py-3 cursor-pointer '
                cssClasses += page===currentPage ? 'bg-[#A6C8FF]' : ''
                return (
                  <li className={cssClasses} onClick={()=>setCurrentPage(page)} key={page}><p>{page}</p></li>
                )
              }
              )}
              {currentPage<8 && <li className='flex-1 py-3 cursor-pointer'>...</li>}
            </ul>
            <button className='bg-inherit border-0' onClick={handleNextPage}>Next</button>
          </section>
        </div>
      </div>
      
    </div>
  )
}

export default Storage