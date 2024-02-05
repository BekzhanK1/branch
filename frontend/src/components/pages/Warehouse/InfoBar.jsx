import React from 'react'

const InfoBar = ({textType, info, style}) => {
    const cssClasses = 'text-left bg-white p-4 '+style
  return (
    <div className={cssClasses}>
        <p>{textType}</p>
        <h4 className='font-bold text-[24px]'>{info}</h4>
    </div>
  )
}

export default InfoBar