import React from 'react'

const Head = ({title, sections}) => {
  return (
    <header className='mb-[1rem]'>
      <h1 className='text-[42px] bg-transparent text-left mb-[24px] font-semibold'>{title}</h1>
      <div className='flex justify-between items-center'>
        <ul type='none' className='flex gap-8 font-semibold'>
          {sections.map(section=>
            <li className='text-[#697077] px-4'>{section}</li>
          )}
        </ul>

        <input type="text" className='w-[238px] h-[48px] bg-white px-4 text-[#C1C7CD]' defaultValue="search"/>
        <button className='bg-sky-600 text-white w-[177px] h-[48px]'>+ Add</button>
      </div>
    </header>
  )
}

export default Head