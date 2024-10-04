import "./App.css";
import { Routes, Route, useNavigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import CreateMeeting from "./pages/CreateMeeting";
import Error404 from "./pages/Error404";
import { useEffect, useState } from "react";
import Register from "./pages/Register";
import Home from "./pages/Home";
function App() {
  const [user, setUser] = useState(true);
  const navigate = useNavigate();

  return (
    <div className="App">
      <Routes>
        <Route path="/" Component={Home} />
        <Route path="/login" Component={Login} />
        <Route path="/register" Component={Register} />
        <Route path="/dashboard" Component={Dashboard} />
        <Route path="/createmeeting" Component={CreateMeeting} />
        <Route path="*" Component={Error404} />
      </Routes>
    </div>
  );
}

export default App;
