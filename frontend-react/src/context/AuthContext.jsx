import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const access = localStorage.getItem("access_token");
    const email = localStorage.getItem("user_email");
    const firstName = localStorage.getItem("user_first_name");
    if (access && email) {
      setUser({ email, first_name: firstName });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
