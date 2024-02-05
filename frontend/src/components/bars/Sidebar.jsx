import React, {useState} from 'react'
import {Link, NavLink} from 'react-router-dom'
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined"
import { MenuItem } from '@mui/material'
import {useSelector} from 'react-redux'
import { useDispatch } from 'react-redux'
import { authActions } from '../store/store'

const Item = ({title, link, icon, selected, setSelected}) => {
  let cssClasses = 'py-2 px-1 '
  cssClasses += selected===title ? 'bg-[#F2F4F8]': 'bg-white'
  return (
    <NavLink to={link}>
      <MenuItem className={cssClasses} onClick={()=>setSelected(title)}>
        {title}
      </MenuItem>
    </NavLink>
  )
}
const Sidebar = () => {
  const [selected, setSelected] = useState('')
  const isAuthorized = useSelector(state=>state.isAuthorized)

  const dispatch = useDispatch()

  const logoutHandle = () =>{
    console.log(localStorage.getItem('token'))
    dispatch(authActions.logout());
    localStorage.removeItem('token')
    console.log(localStorage.getItem('token'))
  }

  return (
    <div className='min-w-[220px] bg-white px-[1rem] py-[2rem] h-[100vh] text-left flex flex-col justify-between'>
        <div>
            <h2 className='text-md text-[1.5rem] font-bold text-[#697077] mb-[16px]'>Branch</h2>
            <input type="text" className='w-full bg-[#F2F4F8] h-[48px] px-4 text-[#C1C7CD]' defaultValue='Search'/>
            <ul className='mt-4 text-[#21272A]'>
                <Item title='Main Page' link='/' selected={selected} setSelected={setSelected}/>
                <Item title='Warehouse' link='/warehouse' selected={selected} setSelected={setSelected}/>
                <Item title='Menu' link='/menu' selected={selected} setSelected={setSelected}/>
                <Item title='Staff' link='/staff' selected={selected} setSelected={setSelected}/>
                <Item title='Info' link='/info' selected={selected} setSelected={setSelected}/>
            </ul>
        </div>
        {!isAuthorized && <NavLink to="login"><button className='bg-[#0F62FE] text-white w-full'>Sign In</button></NavLink>}
        {isAuthorized && <button className='bg-[#0F62FE] text-white w-full' onClick={logoutHandle}>Logout</button>}
    </div>
  )
}

export default Sidebar