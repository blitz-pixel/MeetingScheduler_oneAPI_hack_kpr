import React, { useState } from "react";
import NavBar from "../components/NavBar";
import { Link, useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5001/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        navigate("/dashboard");
      } else {
        alert("Something went wrong!!!!");
      }
    } catch (err) {
      console.log(err);
    }
  };
  return (
    <>
      <NavBar />

      <div className="flex justify-center items-center min-h-screen bg-base-100">
        <div className="p-8 bg-base-300 rounded-lg shadow-md w-full max-w-md mb-10">
          <h1 className="mb-4 font-medium text-center">Login</h1>
          <form>
            <label
              htmlFor="email"
              className="input input-bordered flex items-center gap-2 mb-4"
            >
              <input
                id="email"
                type="text"
                className="grow"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>

            <label
              htmlFor="password"
              className="input input-bordered flex items-center gap-2 mb-4"
            >
              <input
                id="password"
                type="password"
                className="grow"
                placeholder="****"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
            <button className="btn btn-neutral" onClick={handleLogin}>
              Login
            </button>
            <p className="font-light text-gray-400 text-sm mt-4">
              New user?{" "}
              <Link to="/register" className="link link-info">
                Register here
              </Link>
            </p>
          </form>
        </div>
      </div>
    </>
  );
};

export default Login;
