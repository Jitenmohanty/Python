import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import TodoList from "./pages/TodoList";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import { TodoProvider } from "./context/TodoContext";

export default function App() {
  return (
    <AuthProvider>
      <TodoProvider>
      <Router>
        <Navbar />
        <div className="p-4">
          <Routes>
            <Route path="/" element={<Navigate to="/todos" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/todos"
              element={
                <ProtectedRoute>
                  <TodoList />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </Router>
      </TodoProvider>

    </AuthProvider>
  );
}
