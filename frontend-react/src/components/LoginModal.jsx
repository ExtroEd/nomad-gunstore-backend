import React from "react";
import { useState, useEffect } from "react";
import { message } from "antd";
import logo from "../assets/images/logo.png";
import "../assets/styles/LoginModal.css";
import { Link, useNavigate } from 'react-router-dom';
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";


const LoginModal = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [notRobot, setNotRobot] = useState(false);

  const handleLogin = async () => {
    if (!notRobot) {
      return message.error("Please confirm you're not a robot");
    }

    try {
      const res = await fetch(`${API_URL}/api/auth/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();
      if (!res.ok) throw data;

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

      message.success("Logged in successfully!");
      onClose();
      navigate("/customer/account/");
    } catch (err) {
      message.error(err.detail || Object.values(err)?.[0] || "Login failed");
    }
  };

  if (!isOpen) return null;

  return (
    <>
      <div id="login-modal" className="modal-overlay" onClick={onClose}>
        <div className="modal-container" onClick={(e) => e.stopPropagation()}>
          <div className="modal-background-box">
            <div className="modal-content">
              <button className="modal-close" id="close-login-modal" onClick={onClose}>
                &times;
              </button>
              <img src={logo} alt="Logo" className="modal-logo" />
              <h2 className="modal-title">LOG IN</h2>

              <div className="form-group">
                <label>Email<span className="required-asterisk">*</span></label>
                <input
                  type="email"
                  placeholder="Enter Your Email"
                  className="modal-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label>Password<span className="required-asterisk">*</span></label>
                <input
                  type="password"
                  placeholder="Enter Your Password"
                  className="modal-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="recaptcha-box">
                <input
                  type="checkbox"
                  id="recaptcha"
                  checked={notRobot}
                  onChange={(e) => setNotRobot(e.target.checked)}
                />
                <label htmlFor="recaptcha">I'm not a robot</label>
              </div>

              <button className="modal-login-btn" onClick={handleLogin}>Login</button>

              <div className="modal-links-row">
                <a href="/customer/account/forgotpassword/" className="modal-link left" onClick={onClose}>Forgot Password?</a>
                <a href="/customer/account/create" className="modal-link right" onClick={onClose}>Create Account</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <footer className="login-modal-footer">
        <div className="container d-flex justify-content-center align-items-center px-3" style={{ height: "60px" }}>
          <p className="m-0 text-light small text-center w-100">
            &copy; 2025 Nomad Tactical. All Rights Reserved.
          </p>
        </div>
      </footer>
    </>
  );
};

export default LoginModal;
