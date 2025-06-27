import React, { useEffect, useState, useRef } from "react";
import logo from "../assets/images/logo.png";
import "../assets/styles/header.css";
import axios from "axios";
import LoginModal from "./LoginModal";
import { Link } from "react-router-dom";


const Header = () => {
  const [siteSettings, setSiteSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showLogin, setShowLogin] = useState(false);
  const [user, setUser] = useState(null);
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const dropdownRef = useRef();

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

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) setUser(JSON.parse(storedUser));
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownVisible(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
    setDropdownVisible(false);
  };

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

    if (!svgElement) return <span>Invalid SVG</span>;

    const svgHTML = new XMLSerializer().serializeToString(svgElement);
    return <span dangerouslySetInnerHTML={{ __html: svgHTML }} />;
  };

  if (loading) return <div>Loading...</div>;

  return (
    <>
      <header className="header">
        <div className="header-inner container">
          <div className="header-logo">
            <Link to="/" className="logo-link">
              <img src={siteSettings?.logo || logo} alt="Logo" className="logo" />
            </Link>
          </div>

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

          <div className="header-actions">
            {!user ? (
              <button className="header-button login-button" onClick={() => setShowLogin(true)}>
                <span className="icon-wrapper">{renderIcon('login')}</span>
                <span>Log In</span>
              </button>
            ) : (
              <div className="account-wrapper" ref={dropdownRef}>
                <button
                  className="header-button login-button"
                  onClick={() => setDropdownVisible((prev) => !prev)}
                >
                  <span className="icon-wrapper">{renderIcon('login')}</span>
                  <span>My Account</span>
                </button>
                {dropdownVisible && (
                  <div className="account-dropdown">
                    <div className="account-welcome">Welcome, {user.first_name}</div>
                    <div className="dropdown-divider" />
                    <ul className="dropdown-list">
                      <li><Link to="/account">My Account</Link></li>
                      <li><Link to="/address-book">Address Book</Link></li>
                      <li><Link to="/payments">Saved Payments</Link></li>
                      <li><Link to="/preferred-ffl">Preferred FFL</Link></li>
                      <li><Link to="/order-history">Order History</Link></li>
                      <li><Link to="/wishlists">Wishlists</Link></li>
                      <li><Link to="/saved-for-later">Saved for Later</Link></li>
                      <li><Link to="/help-center">Help Center</Link></li>
                    </ul>
                    <div className="dropdown-divider" />
                    <button className="logout-button" onClick={handleLogout}>Log Out</button>
                  </div>
                )}
              </div>
            )}

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

      {showLogin && <LoginModal isOpen={showLogin} onClose={() => setShowLogin(false)} setUser={setUser} />}
    </>
  );
};

export default Header;
