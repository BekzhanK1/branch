import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route,createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Login from "./components/pages/Login.jsx";
import Signup from "./components/pages/Signup.jsx";
import Panel from "./components/pages/Panel.jsx";
import Main from "./components/pages/Main/Main";
import RootLayout from "./RootLayout";
import Analytics from "./components/pages/Main/Analytics";
import Warehouse from "./components/pages/Warehouse/Warehouse";
import Menu from "./components/pages/Menu/Menu";
import StaffLayout from "./components/pages/Staff/StaffLayout";
import Customers from "./components/pages/Staff/Customers";
import Staff from "./components/pages/Staff/Staff";
import KPI from "./components/pages/Staff/KPI";

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout/>,
    children: [
      {
        path:'/', 
        element: <Main/>, 
        children: [
          {path:'analytics', element:<Analytics/>},
          {path: 'admin'},
          {path: ':cellId'}
        ]
      },
      {
        path: 'warehouse',
        element: <Warehouse/>,
        children: [
          {path:':cellId'}
        ]
      },
      {
        path: 'menu',
        element: <Menu/>,
        children: [
          {path:':cellId'}
        ]
      },
      {
        path: 'staff',
        element: <StaffLayout/>,
        children: [
          {path:'customers',element: <Customers/>},
          {path:'workers', element: <Staff/>},
          {path: 'kpi', element: <KPI/>}
        ]
      },
      {
        path: 'login',
        element: <Login/>
      },
      {
        path: 'signup',
        element: <Signup/>
      },
      {
        path: 'panel',
        element: <Panel/>
      }
    ]
  }
])


ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
      <RouterProvider router={router}/>
    </React.StrictMode>
);
