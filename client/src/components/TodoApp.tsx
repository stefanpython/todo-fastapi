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
    <div>
      <h2>Todo List</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter a task"
        />
        <button type="submit">Add Todo</button>
      </form>
      <ul>
        {todos.map((todo: { task: string }, idx) => (
          <li key={idx}>{todo.task}</li>
        ))}
      </ul>
    </div>
  );
}
