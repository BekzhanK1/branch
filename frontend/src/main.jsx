import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./index.css";
import Login from "./components/pages/Login.jsx";
import Signup from "./components/pages/Signup.jsx";
import Panel from "./components/pages/Panel.jsx";
import Storage from "./components/pages/Storage/Storage";
import Main from "./components/pages/Main/Main";
ReactDOM.createRoot(document.getElementById("root")).render(
  <Router>
    <React.StrictMode>
      <Routes>
        {" "}
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/panel" element={<Panel />} />
        <Route path="/storage" element={<Storage />} />
        <Route path="/" element={<Main />} />
      </Routes>
    </React.StrictMode>
  </Router>
);
