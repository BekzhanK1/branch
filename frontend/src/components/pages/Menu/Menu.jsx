import React, { useEffect, useState } from 'react'
import classes from './Menu.module.css'
import Head from '../../bars/Head'
import Sidebar from '../../bars/Sidebar'

import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import { Button, gridClasses } from '@mui/material'
import { grey } from '@mui/material/colors'
import axios from 'axios';
import {useSelector } from 'react-redux';

const columns = [
  { field: 'name', headerName: 'Name', flex:1.5 },
  {
    field: 'date',
    headerName: 'Date',
    flex: 1,
    editable: true,
  },
  {
    field: 'quantity',
    headerName: 'Quantity',
    flex: 1,
    editable: true,
  },
  {
    field: 'price',
    headerName: 'Price',
    headerAlign: 'left',
    type: 'number',
    flex: 1,
    editable: true,
  },
  {
    field: 'totalPrice',
    headerName: 'Total Price',
    headerAlign: 'left',
    type: 'number',
    flex: 1,
    editable: true,
  },
  {
    field: 'status',
    headerName: 'Status',
    fontWeight: 'bold',
    description: 'This column has a value getter and is not sortable.',
    sortable: false,
    flex: 1,
    renderCell: ()=>(
      <div>love</div>
    )
  },
  {
    field: 'actions',
    type: 'actions',
    headerName:'Actions',
    headerAlign: 'center',
    cellClassName: 'actions',
    sortable: false,
    flex: 0.5,
    renderCell: ()=>(
      <button style={{backgroundColor:'transparent', fontSize:'20px',border:0 }}>
        ...
      </button>
    )
  }
];

const rows = [
  { id:1, name: 1, date: 'Snow', quantity: 10, price: 14,totalPrice:140, status:'Baige' },
  { id:2, name: 2, date: 'Lannister', quantity: 20, price: 31,totalPrice:620, status:'Baige' },
  { id:3, name: 3, date: 'Lannister', quantity: 9, price: 31,totalPrice:279, status:'Baige' },
  { id:4, name: 4, date: 'Stark', quantity: 11, price: 11,totalPrice:121, status:'Baige' },
  { id:5, name: 5, date: 'Targaryen', quantity: 15, price: 10,totalPrice:150, status:'Baige' },
  { id:6, name: 6, date: 'Melisandre', quantity: 9, price: 150,totalPrice:1350, status:'Baige' },
  { id:7, name: 7, date: 'Clifford', quantity: 89, price: 10,totalPrice:890, status:'Baige' },
  { id:8, name: 8, date: 'Frances', quantity: 30, price: 23,totalPrice:690, status:'Baige' },
  { id:9, name: 9, date: 'Roxie', quantity: 12, price: 65,totalPrice:780, status:'Baige' },
];



const Menu = () => {
  
  const isAuth = useSelector(state=>state.isAuthorized)
  console.log(isAuth)
  //console.log(axios.defaults.headers.common['Authorization'])
  
  const [error, setError] = useState(null)


  useEffect(()=>{
    if (isAuth){
      console.log(axios)
      axios.get(`http://127.0.0.1/api/menu`)
      .then((response) => response.json()).then((data)=>console.log(data))
      .catch((error) => {
        switch (error.response ? error.response.status : null) {
          case 400:
            console.error("Incorrect login or password");
            setError("Incorrect login or password");
            break;
          case 401:
            console.error("Unauthorized access");
            setError("Unauthorized access");
            break;
          default:
            if (error.request) {
              console.error(
                "Timeout. The server is unavailable. Please contact the administrator"
              );
              setError(
                "Timeout. The server is unavailable. Please contact the administrator"
              );
            } else {
              console.error("Authentication error:", error);
              setError("Authentication error");
            }
            break;
        }
      });
    }
  },[isAuth]);
  
  return (
    <div className='bg-[#DDE1E6] left-0 right-0 text-[#21272A] flex relative box-border flex-1'>
      <div className='h-full p-[24px] left-0 right-0 w-full'>
        <Head title='Menu' sections={[{title:'Cell', id:1, path: 'cell1'},{title: 'Cell',id:2,path:'cell2'},{title:'Cell',id:3,path:'cell3'},{title:'Cell',id:4,path:'cell4'}]}></Head>
        <div className='mt-[20px] h-[60vh]'>
          {error && <p>{error}</p>}
          {!error && <Box sx={{ 
            height: 'fit',
            width: '100%', 
            borderRadius:0,
            backgroundColor:'#F2F4F8',
            textAlign: 'left',
            }}>
            <DataGrid
              rows={rows}
              columns={columns}
              getCellClassName={(params) => {
                return 'usualCell';
              }}
              initialState={{
                pagination: {
                  paginationModel: {
                    pageSize: 8,
                  },
                },
              }}
              sx={{
                border: 0.5,
                borderColor: '#F2F4F8',
                fontSize: 16,
                borderRadius:0,
                '& .MuiDataGrid-cell': {
                  backgroundColor: 'white',
                },
              }}
              pageSizeOptions={[8,10,15]}
              checkboxSelection
              disableRowSelectionOnClick
            />
          </Box>}
        </div>
      </div>
    </div>
  )
}

export default Menu