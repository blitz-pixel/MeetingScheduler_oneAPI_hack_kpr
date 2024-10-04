import React from "react";
import NavBar from "../components/NavBar";
import { Link, useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();
  const handleRegister = () => {
    navigate("/login");
  };
  return (
    <>
      <NavBar />

      <div className="flex justify-center items-center min-h-screen bg-base-100">
        <div className="p-8 bg-base-300 rounded-lg shadow-md w-full max-w-md mb-10">
          <h1 className="mb-4 font-medium text-center">Register</h1>
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
              />
            </label>
            <button className="btn btn-neutral" onClick={handleRegister}>
              Register
            </button>
            <p className="font-light text-gray-400 text-sm mt-4">
              Have account?{" "}
              <Link to="/login" className="link link-info">
                Login
              </Link>
            </p>
          </form>
        </div>
      </div>
    </>
  );
};

export default Register;
