export const login = async (username: string, password: string) => {
  const response = await fetch("http://127.0.0.1:8000/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password, grant_type: "password" }),
  });

  if (!response.ok) throw new Error("Invalid credentials");

  const data = await response.json();
  localStorage.setItem("token", data.access_token);
};

export const register = async (username: string, password: string) => {
  const response = await fetch("http://127.0.0.1:8000/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Send JSON
    },
    body: JSON.stringify({ username, password }), // Send as JSON
  });

  if (!response.ok) {
    throw new Error("Registration failed");
  }
};

export const logout = () => {
  localStorage.removeItem("token");
};

export const getAuthHeaders = (): Record<string, string> => {
  const token = localStorage.getItem("token");
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "", // Return an empty string if token is missing
  };
};

export const isAuthenticated = () => !!localStorage.getItem("token");
