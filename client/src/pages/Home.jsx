import React from "react";
import { Link } from "react-router-dom"; // Use react-router-dom for navigation
import NavBar from "../components/NavBar"; // Import the NavBar component

export default function Home() {
  return (
    <main className="bg-base-100 min-h-screen flex flex-col">
      <NavBar />
      <div className="p-4 flex-grow flex flex-col justify-center items-start ml-10">
        <h1 className="font-extrabold text-4xl">AI Meeting Scheduler</h1>
        <p className="mt-2 text-lg">
          Optimize Your Time with AI-Powered Scheduling
        </p>
        <Link to="/login" className="btn btn-neutral mt-4">
          Start now
        </Link>
      </div>
    </main>
  );
}
