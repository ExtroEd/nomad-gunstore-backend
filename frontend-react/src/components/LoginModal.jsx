import React from "react";
import logo from "../assets/images/logo.png";
import "../assets/styles/LoginModal.css";
import { Link } from 'react-router-dom';


const LoginModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <>
      <div id="login-modal" className="modal-overlay" onClick={onClose}>
        <div className="modal-container" onClick={(e) => e.stopPropagation()}>
          <div className="modal-background-box">
            <div className="modal-content">
              <button className="modal-close" id="close-login-modal" onClick={onClose}>&times;</button>
              <img src={logo} alt="Logo" className="modal-logo" />
              <h2 className="modal-title">LOG IN</h2>

              <div className="form-group">
                <label>
                  Email<span className="required-asterisk">*</span>
                </label>
                <input type="email" placeholder="Enter Your Email" className="modal-input" />
              </div>

              <div className="form-group">
                <label>
                  Password<span className="required-asterisk">*</span>
                </label>
                <input type="password" placeholder="Enter Your Password" className="modal-input" />
              </div>

              <div className="recaptcha-box">
                <input type="checkbox" id="recaptcha" />
                <label htmlFor="recaptcha">I'm not a robot</label>
              </div>

              <button className="modal-login-btn">Login</button>

              <div className="modal-links-row">
                <Link
                  to="/customer/account/forgotpassword/"
                  className="modal-link left"
                  onClick={onClose}
                >
                  Forgot Password?
                </Link>
                <Link
                  to="/customer/account/create"
                  className="modal-link right"
                  onClick={onClose}
                >
                  Create Account
                </Link>
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
