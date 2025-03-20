import { useState, useEffect } from "react";
import { getAuthHeaders, logout } from "../auth";

interface Todo {
  task: string;
  completed: boolean;
}

export default function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [task, setTask] = useState("");
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

  // Load todos on mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = () => {
    fetch("http://127.0.0.1:8000/todos/", {
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(), // Spread the headers to ensure they are valid
      },
    })
      .then((res) => res.json())
      .then((data) => setTodos(data))
      .catch((err) => console.error("Error fetching:", err));
  };

  const handleLogout = () => {
    logout();
    window.location.href = "/login";
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (editingIndex !== null) {
      // We're updating
      handleUpdateSubmit();
    } else {
      // We're adding new
      handleAddSubmit();
    }
  };

  const handleAddSubmit = () => {
    const newTodo: Todo = { task, completed: false };

    fetch("http://127.0.0.1:8000/todos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(), // Spread the headers to ensure they are valid
      },
      body: JSON.stringify(newTodo),
    })
      .then((res) => res.json())
      .then(() => {
        // Refresh todos from server to ensure sync
        fetchTodos();
        setTask("");
      })
      .catch((err) => console.error("Error adding:", err));
  };

  const handleUpdateSubmit = () => {
    if (editingIndex === null) return;

    const updatedTodo: Todo = {
      task,
      completed: todos[editingIndex].completed,
    };

    fetch(`http://127.0.0.1:8000/todos/${editingIndex}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(), // Spread the headers to ensure they are valid
      },
      body: JSON.stringify(updatedTodo),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Server response: ${res.status}`);
        }
        return res.json();
      })
      .then(() => {
        // Refresh todos from server to ensure sync
        fetchTodos();
        setTask("");
        setEditingIndex(null);
      })
      .catch((err) => console.error("Error updating:", err));
  };

  const handleDelete = (index: number) => {
    fetch(`http://127.0.0.1:8000/todos/${index}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(), // Spread the headers to ensure they are valid
      },
    })
      .then((res) => res.json())
      .then(() => {
        // Refresh todos from server
        fetchTodos();
      })
      .catch((err) => console.error("Error deleting:", err));
  };

  const handleEdit = (index: number) => {
    const todo = todos[index];
    setTask(todo.task);
    setEditingIndex(index);
  };

  const handleCancelEdit = () => {
    setTask("");
    setEditingIndex(null);
  };

  const handleToggleComplete = (index: number) => {
    const todo = todos[index];
    const updatedTodo = { ...todo, completed: !todo.completed };

    fetch(`http://127.0.0.1:8000/todos/${index}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(), // Spread the headers to ensure they are valid
      },
      body: JSON.stringify(updatedTodo),
    })
      .then((res) => res.json())
      .then(() => {
        fetchTodos();
      })
      .catch((err) => console.error("Error toggling:", err));
  };

  return (
    <div className="bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-gray-800">Todo List</h2>
          <button
            onClick={handleLogout}
            className="p-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Logout
          </button>
        </div>
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
            {editingIndex === null ? "Add Todo" : "Update Todo"}
          </button>
          {editingIndex !== null && (
            <button
              type="button"
              onClick={handleCancelEdit}
              className="ml-2 p-2 bg-gray-400 text-white rounded-md hover:bg-gray-500"
            >
              Cancel
            </button>
          )}
        </form>

        <ul className="space-y-3">
          {todos.map((todo, idx) => (
            <li
              key={idx}
              className="p-3 bg-gray-50 rounded-md shadow-sm hover:bg-gray-200"
            >
              <div className="flex items-center justify-between">
                <span
                  className={`flex-grow ${
                    todo.completed ? "line-through text-gray-500" : ""
                  }`}
                >
                  {todo.task}
                </span>
                <div className="space-x-2">
                  <button
                    onClick={() => handleEdit(idx)}
                    className="px-3 py-1 bg-yellow-500 text-white rounded-md hover:bg-yellow-600"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(idx)}
                    className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600"
                  >
                    Delete
                  </button>
                  <button
                    onClick={() => handleToggleComplete(idx)}
                    className={`px-3 py-1 ${
                      todo.completed ? "bg-green-500" : "bg-blue-500"
                    } text-white rounded-md hover:bg-opacity-80`}
                  >
                    {todo.completed ? "Mark Incomplete" : "Mark Complete"}
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
