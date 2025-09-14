import { createContext, useContext, useState, useEffect } from "react";
import API from "../api";
import { useAuth } from "./AuthContext";

const TodoContext = createContext();

export function TodoProvider({ children }) {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  // ✅ fetch all todos on mount
  useEffect(() => {
    if (!token) return; // don’t fetch if not logged in
    const fetchTodos = async () => {
      setLoading(true);
      try {
        const res = await API.get("/todos", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTodos(res.data);
      } catch (err) {
        console.error("Failed to fetch todos", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTodos();
  }, [token]);

  // ✅ add todo locally
  const addTodo = async (newTodo) => {
    setLoading(true);
    try {
      const res = await API.post("/todos", newTodo, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTodos((prev) => [...prev, res.data]); // push new todo into state
    } catch (err) {
      console.error("Failed to add todo", err);
    } finally {
      setLoading(false);
    }
  };

  // ✅ update todo locally
  const updateTodo = async (id, updatedData) => {
    setLoading(true);
    try {
      const res = await API.put(`/todos/${id}`, updatedData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTodos((prev) =>
        prev.map((t) => (t.id === id ? res.data : t))
      );
    } catch (err) {
      console.error("Failed to update todo", err);
    } finally {
      setLoading(false);
    }
  };

  // ✅ delete todo locally
  const deleteTodo = async (id) => {
    setLoading(true);
    try {
      await API.delete(`/todos/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTodos((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      console.error("Failed to delete todo", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <TodoContext.Provider
      value={{ todos, loading, addTodo, updateTodo, deleteTodo }}
    >
      {children}
    </TodoContext.Provider>
  );
}

export function useTodos() {
  return useContext(TodoContext);
}
