import React,{useState} from 'react'
import {Bar,Line} from 'react-chartjs-2'
import { chartData } from '../../../data/chartData';
import { Chart as ChartJS } from "chart.js/auto";
const Analytics = () => {
    const [userData, setUserData] = useState({
        labels: chartData.map(row=>row.year),
        datasets: [
        {
            label: 'Current Year',
            data: chartData.map(data=>data.userGain)
        },
        {
            label: 'Previous Year',
            data: chartData.map(data=>data.userGain)
          }
    ]
      })
    return (
        <section className='flex w-full gap-[1rem] flex-wrap'>
            <div className='w-[calc(50%-0.5rem)] bg-white p-4 h-[300px] hover:cursor-pointer'>
                <Bar data={userData} options={{responsive:true}}></Bar>
            </div>
            <div className='w-[calc(50%-0.5rem)] bg-white p-4 h-[300px] hover:cursor-pointer'>
                <Line data={userData} options={{responsive:true}}></Line>
            </div>
            <div className='w-[calc(50%-0.5rem)] bg-white p-4 h-[300px] hover:cursor-pointer'>
                <Bar data={userData} options={{responsive:true}}></Bar>
            </div>
            <div className='w-[calc(50%-0.5rem)] bg-white p-4 h-[300px] hover:cursor-pointer'>
                <Line data={userData} options={{responsive:true}}></Line>
            </div>
        
        </section>
    )
}

export default Analytics