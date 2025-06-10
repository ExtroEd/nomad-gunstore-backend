import React from "react";
import logo from "../assets/images/logo.png";


const LoginModal = () => {
  return (
    <div id="login-modal" className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" id="close-login-modal">&times;</button>
        <img src={logo} alt="Logo" className="modal-logo" />
        <h2 className="modal-title">Log In</h2>
        <label>Email*</label>
        <input type="email" placeholder="Enter Your Email" className="modal-input" />
        <label>Password</label>
        <input type="password" placeholder="Enter Your Password" className="modal-input" />
        <div className="recaptcha-box">
          <input type="checkbox" id="recaptcha" />
          <label htmlFor="recaptcha">I'm not a robot</label>
        </div>
        <button className="modal-login-btn">Login</button>
        <div className="modal-links">
          <a href="#" className="modal-link">Forgot Password?</a>
          <a href="#" className="modal-link">Create Account</a>
        </div>
        <footer className="modal-footer">
          © 2025 Nomad Tactical. All rights reserved.
        </footer>
      </div>
    </div>
  );
};

export default LoginModal;
