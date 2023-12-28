import React, {useState} from 'react'
import {Link} from 'react-router-dom'
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined"
import { MenuItem } from '@mui/material'
const Item = ({title, link, icon, selected, setSelected}) => {
  let cssClasses = 'py-2 px-1 '
  cssClasses += selected===title ? 'bg-[#F2F4F8]': 'bg-white'
  return (
    <MenuItem className={cssClasses} onClick={()=>setSelected(title)}>
      <Link to={link}>{title}</Link>
    </MenuItem>
  )
}
const Sidebar = () => {
  const [selected, setSelected] = useState('')
  return (
    <div className='w-[256px] bg-white px-[1rem] py-[2rem] h-full text-left flex flex-col justify-between'>
        <div>
            <h2 className='text-md text-[1.5rem] font-bold text-[#697077] mb-[16px]'>Branch</h2>
            <input type="text" className='w-full bg-[#F2F4F8] h-[48px] px-4 text-[#C1C7CD]' defaultValue='Search'/>
            <ul className='mt-4 text-[#21272A]'>
                <Item title='Main Page' link='/' selected={selected} setSelected={setSelected}/>
                <Item title='Storage' link='/storage' selected={selected} setSelected={setSelected}/>
                <Item title='Menu' link='/menu' selected={selected} setSelected={setSelected}/>
                <Item title='Staff' link='/panel' selected={selected} setSelected={setSelected}/>
                <Item title='Info' link='/info' selected={selected} setSelected={setSelected}/>
            </ul>
        </div>
        <button className='bg-[#0F62FE] text-white w-full'>Sign In</button>
    </div>
  )
}

export default Sidebar