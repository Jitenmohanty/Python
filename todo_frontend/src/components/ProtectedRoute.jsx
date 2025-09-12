import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();

  if (token === undefined) return null; // wait until token is loaded
  if (!token) return <Navigate to="/login" replace />;

  return children;
}
