import React from "react";
import DashboadrNav from "../components/DashboardNav";
import MyCalendar from "../components/MyCalendar"; // Import your calendar component

const Dashboard = () => {
  // Example events data (you can fetch this from your API)
  const myEventsList = [
    {
      id: 0,
      title: "Board meeting",
      start: new Date(2024, 9, 5, 10, 0), // Year, Month (0-indexed), Day, Hour, Minute
      end: new Date(2024, 9, 5, 12, 0),
    },
    {
      id: 1,
      title: "Conference",
      start: new Date(2024, 9, 7, 10, 0),
      end: new Date(2024, 9, 7, 14, 0),
    },
    // Add more events here as needed
  ];

  return (
    <>
      <DashboadrNav />
      <div style={{ marginTop: "20px" }}>
        <h2>My Google Calendar</h2>
        <MyCalendar myEventsList={myEventsList} />{" "}
      </div>
    </>
  );
};

export default Dashboard;
