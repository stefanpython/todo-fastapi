import { useState, useEffect } from "react";

export default function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/todos/")
      .then((res) => res.json())
      .then((data) => setTodos(data));
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newTodo = { task, completed: false };
    fetch("http://127.0.0.1:8000/todos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newTodo),
    })
      .then((res) => res.json())
      .then(() => {
        setTodos((prevTodos) => [...prevTodos, newTodo] as typeof prevTodos);
        setTask("");
      });
  };

  return (
    <div className=" bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">
          Todo List React + FastApi
        </h2>
        <form onSubmit={handleSubmit} className="flex mb-6">
          <input
            type="text"
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Enter a task"
            className="flex-grow p-2 rounded-l-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add Todo
          </button>
        </form>
        <ul className="space-y-3">
          {todos.map((todo: { task: string }, idx) => (
            <li
              key={idx}
              className="p-3 bg-gray-50 rounded-md shadow-sm hover:bg-gray-200"
            >
              {todo.task}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
