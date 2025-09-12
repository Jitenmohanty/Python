import { useEffect, useState } from "react";
import API from "../api";

export default function TodoList() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  const fetchTodos = async () => {
    try {
      const res = await API.get("/todos");
      setTodos(res.data);
    } catch (err) {
      alert("Failed to fetch todos");
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await API.post("/todos", { title });
      setTitle("");
      fetchTodos();
    } catch (err) {
      alert("Failed to add todo");
    }
  };

  const handleDelete = async (id) => {
    try {
      await API.delete(`/todos/${id}`);
      fetchTodos();
    } catch (err) {
      alert("Failed to delete todo");
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">Todo List</h2>
      <form onSubmit={handleAdd} className="flex space-x-2 mb-4">
        <input
          type="text"
          placeholder="Add a todo"
          className="flex-grow p-2 border rounded"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Add
        </button>
      </form>
      <ul className="space-y-2">
        {todos.map((todo) => (
          <li key={todo.id} className="flex justify-between p-2 border rounded">
            <span>{todo.title}</span>
            <button
              onClick={() => handleDelete(todo.id)}
              className="text-red-600 hover:underline"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
