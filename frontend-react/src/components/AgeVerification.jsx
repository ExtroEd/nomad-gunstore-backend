import React from "react";
import logo from ".../public/logo.png";


const AgeVerification = () => {
  return (
    <div id="age-verification-overlay">
      <div className="age-verification-popup">
        <img src={logo} alt="Logo" className="popup-logo" />
        <p className="popup-subtitle">
          Welcome to Nomad Tactical, our site is intended for individuals of at least 18 years of age.
        </p>
        <p className="popup-title">Are you at least 18 years old?</p>
        <div className="popup-buttons">
          <button id="yes-button">Yes</button>
          <button id="no-button">No</button>
        </div>
        <label className="popup-checkbox">
          <input type="checkbox" id="remember-check" />
          <span>
            I verify that this device is not shared.<br />Remember me temporarily while I shop.
          </span>
        </label>
      </div>
    </div>
  );
};

export default AgeVerification;
