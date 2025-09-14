import { useState } from "react";
import { useTodos } from "../context/TodoContext";
import Loader from "../components/Loader";

export default function TodoList() {
  const { todos, loading, addTodo, updateTodo, deleteTodo } = useTodos();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [editingId, setEditingId] = useState(null);

  const handleAddOrEdit = async (e) => {
    e.preventDefault();
    if (editingId) {
      await updateTodo(editingId, { title, description });
      setEditingId(null);
    } else {
      await addTodo({ title, description });
    }
    setTitle("");
    setDescription("");
  };

  const handleEdit = (todo) => {
    setEditingId(todo.id);
    setTitle(todo.title);
    setDescription(todo.description || "");
  };

  const toggleComplete = async (todo) => {
    await updateTodo(todo.id, {
      title: todo.title,
      description: todo.description,
      completed: !todo.completed,
    });
  };

  return (
    <div className="max-w-lg mx-auto mt-10">
      {loading && <Loader />}
      <h2 className="text-2xl font-bold mb-4">Todo List</h2>
      <form onSubmit={handleAddOrEdit} className="space-y-2 mb-4">
        <input
          type="text"
          placeholder="Title"
          className="w-full p-2 border rounded"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          className="w-full p-2 border rounded"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          {editingId ? "Update Todo" : "Add Todo"}
        </button>
      </form>

      <ul className="space-y-2">
        {todos.map((todo) => (
          <li
            key={todo.id}
            className={`flex justify-between items-center p-2 border rounded ${
              todo.completed ? "bg-green-100" : ""
            }`}
          >
            <div>
              <span className="font-semibold">{todo.title}</span>
              {todo.description && (
                <p className="text-sm text-gray-600">{todo.description}</p>
              )}
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => toggleComplete(todo)}
                className={`px-2 py-1 rounded ${
                  todo.completed ? "bg-gray-300" : "bg-green-600 text-white"
                }`}
              >
                {todo.completed ? "Undo" : "Complete"}
              </button>
              <button
                onClick={() => handleEdit(todo)}
                className="px-2 py-1 bg-yellow-400 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="px-2 py-1 bg-red-600 text-white rounded"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
