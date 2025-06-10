import React, { useState, useEffect } from 'react';
import logo from "../assets/images/logo.png";


const AgeVerification = () => {
  const [showOverlay, setShowOverlay] = useState(true);
  const [remember, setRemember] = useState(false);

  useEffect(() => {
    if (sessionStorage.getItem('ageVerified') === 'true') {
      setShowOverlay(false);
    }
  }, []);

  const handleYes = () => {
    if (remember) {
      sessionStorage.setItem('ageVerified', 'true');
    }
    setShowOverlay(false);
  };

    const handleNo = () => {
      window.open('https://cbd.minjust.gov.kg/214/edition/10704/ru', '_blank');
    };

  if (!showOverlay) return null;

  return (
    <div id="age-verification-overlay" style={{
      position: 'fixed', top:0, left:0, right:0, bottom:0,
      backgroundColor: 'rgba(0,0,0,0.8)', display: 'flex',
      justifyContent: 'center', alignItems: 'center', zIndex: 9999
    }}>
      <div className="age-verification-popup" style={{ backgroundColor: 'white', padding: 20, borderRadius: 8, maxWidth: 400, textAlign: 'center' }}>
        <img src={logo} alt="Logo" className="popup-logo" />
        <p className="popup-subtitle">
          Welcome to Nomad Tactical, our site is intended for individuals of at least 18 years of age.
        </p>
        <p className="popup-title">Are you at least 18 years old?</p>
        <div className="popup-buttons" style={{ marginBottom: 20 }}>
          <button id="yes-button" onClick={handleYes} style={{ marginRight: 10 }}>Yes</button>
          <button id="no-button" onClick={handleNo}>No</button>
        </div>
        <label className="popup-checkbox" style={{ cursor: 'pointer' }}>
          <input
            type="checkbox"
            id="remember-check"
            checked={remember}
            onChange={e => setRemember(e.target.checked)}
          />
          <span>
            I verify that this device is not shared.<br />Remember me temporarily while I shop.
          </span>
        </label>
      </div>
    </div>
  );
};

export default AgeVerification;
