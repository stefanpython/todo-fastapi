export const login = async (username: string, password: string) => {
  const response = await fetch("http://127.0.0.1:8000/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password }),
  });

  if (!response.ok) throw new Error("Invalid credentials");

  const data = await response.json();
  localStorage.setItem("token", data.access_token);
};

export const logout = () => {
  localStorage.removeItem("token");
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const isAuthenticated = () => !!localStorage.getItem("token");
