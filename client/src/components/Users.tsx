import { useState, useEffect } from "react";

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/users/4") // Change the endpoint if needed
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched data:", data); // Check the response data
        setUsers([data]);
      })
      .catch((error) => console.error("Error fetching users:", error)); // Log any errors
  }, []);

  return (
    <div>
      <h2>User List</h2>
      {users.map((user, idx) => (
        <p key={idx}>{user.name}</p>
      ))}
    </div>
  );
}
