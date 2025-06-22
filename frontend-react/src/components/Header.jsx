import React, { useEffect, useState } from "react";
import logo from "../assets/images/logo.png";
import "../assets/styles/header.css";
import axios from "axios";
import LoginModal from "./LoginModal";
import { Link } from "react-router-dom";


const Header = () => {
  const [siteSettings, setSiteSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showLogin, setShowLogin] = useState(false);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await axios.get(`/api/site-settings/?t=${Date.now()}`);
        setSiteSettings(response.data);
      } catch (error) {
        console.error("Error fetching site settings:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const renderIcon = (iconType) => {
    if (!siteSettings?.icons?.[iconType]) {
      const fallbackIcons = {
        search: "/images/search-icon.svg",
        login: "/images/account-icon.svg",
        help: "/images/customer-service-icon.svg",
        cart: "/images/cart-icon.svg"
      };
      return <img src={fallbackIcons[iconType]} alt={`${iconType} icon`} />;
    }

    const svgString = siteSettings.icons[iconType];
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
    const svgElement = svgDoc.querySelector('svg');

    if (!svgElement) {
      return <span>Invalid SVG</span>;
    }

    const svgHTML = new XMLSerializer().serializeToString(svgElement);
    return <span dangerouslySetInnerHTML={{ __html: svgHTML }} />;
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <header className="header">
        <div className="header-inner container">

          {/* Логотип слева */}
          <div className="header-logo">
            <Link to="/" className="logo-link">
              <img
                src={siteSettings?.logo || logo}
                alt="Logo"
                className="logo"
              />
            </Link>
          </div>

          {/* Центр: строка поиска */}
          <form className="header-search">
            <input
              type="text"
              className="search-input"
              placeholder={`Search Nomad Tactical by Keywords...`}
            />
            <button type="submit" className="search-button">
              <span className="icon-wrapper">{renderIcon('search')}</span>
            </button>
          </form>

          {/* Кнопки справа */}
          <div className="header-actions">
            <button className="header-button login-button" onClick={() => setShowLogin(true)}>
              <span className="icon-wrapper">{renderIcon('login')}</span>
              <span>Log In</span>
            </button>

            <div className="divider" />

            <Link to="/help-center/terms-conditions" className="header-button link-button">
              <span className="icon-wrapper">{renderIcon('help')}</span>
              <span>Help Center</span>
            </Link>

            <div className="divider" />

            <Link to="/checkout/cart" className="header-button link-button">
              <span className="icon-wrapper">{renderIcon('cart')}</span>
              <span>View Cart</span>
            </Link>
          </div>
        </div>
      </header>

      {showLogin && <LoginModal isOpen={showLogin} onClose={() => setShowLogin(false)} />}
    </>
  );
};

export default Header;
